const FileProcessor = require('../../src/services/fileProcessor');
const fs = require('fs-extra');
const path = require('path');

describe('FileProcessor', () => {
  let fileProcessor;
  
  beforeEach(() => {
    fileProcessor = new FileProcessor();
  });

  describe('constructor', () => {
    test('should initialize with supported formats', () => {
      expect(fileProcessor.supportedFormats).toEqual(['.yaml', '.yml', '.txt', '.md']);
    });
  });

  describe('parseYamlFile', () => {
    test('should parse valid YAML content', () => {
      const yamlContent = `
url: https://example.com
title: Test Title
meta_description: Test description
meta_keywords:
  - keyword1
  - keyword2
`;
      
      const result = fileProcessor.parseYamlFile(yamlContent);
      
      expect(result.url).toBe('https://example.com');
      expect(result.title).toBe('Test Title');
      expect(result.meta_description).toBe('Test description');
      expect(result.meta_keywords).toEqual(['keyword1', 'keyword2']);
    });

    test('should parse YAML with frontmatter and content', () => {
      const content = `---
url: https://example.com
title: Test Title
---
This is the main content`;

      const result = fileProcessor.parseYamlFile(content);
      
      expect(result.url).toBe('https://example.com');
      expect(result.title).toBe('Test Title');
      expect(result.content).toBe('This is the main content');
    });

    test('should throw error for invalid YAML', () => {
      const invalidYaml = `
url: https://example.com
title: Test Title
  invalid: yaml: structure:
`;
      
      expect(() => {
        fileProcessor.parseYamlFile(invalidYaml);
      }).toThrow('Ошибка парсинга YAML');
    });
  });

  describe('parseMarkdownFile', () => {
    test('should parse markdown with frontmatter', () => {
      const markdownContent = `---
url: https://example.com
title: Test Title
meta_keywords:
  - test
  - markdown
---

# Main Content

This is the main content of the page.`;

      const result = fileProcessor.parseMarkdownFile(markdownContent);
      
      expect(result.url).toBe('https://example.com');
      expect(result.title).toBe('Test Title');
      expect(result.meta_keywords).toEqual(['test', 'markdown']);
      expect(result.content).toContain('# Main Content');
    });

    test('should extract data from plain markdown without frontmatter', () => {
      const plainMarkdown = `# Test Title

This is content without frontmatter.
URL: https://example.com
Keywords: test, markdown`;

      const result = fileProcessor.parseMarkdownFile(plainMarkdown);
      
      expect(result.title).toBe('# Test Title');
      expect(result.content).toBe(plainMarkdown);
    });
  });

  describe('extractDataFromText', () => {
    test('should extract data from structured text', () => {
      const textContent = `URL: https://example.com
Title: Test Title
Description: Test description
Keywords: keyword1, keyword2

Main content here`;

      const result = fileProcessor.extractDataFromText(textContent);
      
      expect(result.url).toBe('https://example.com');
      expect(result.title).toBe('Test Title');
      expect(result.meta_description).toBe('Test description');
      expect(result.meta_keywords).toEqual(['keyword1', 'keyword2']);
    });

    test('should handle missing fields gracefully', () => {
      const textContent = `Some content without structured data`;

      const result = fileProcessor.extractDataFromText(textContent);
      
      expect(result.title).toBe('Some content without structured data');
      expect(result.url).toBe('');
      expect(result.meta_keywords).toEqual([]);
    });
  });

  describe('validateData', () => {
    test('should pass validation for valid data', () => {
      const validData = {
        url: 'https://example.com',
        title: 'Test Title',
        meta_description: 'Test description',
        meta_keywords: ['keyword1', 'keyword2'],
        main_keyword: 'keyword1'
      };

      expect(() => {
        fileProcessor.validateData(validData);
      }).not.toThrow();
    });

    test('should throw error for missing required fields', () => {
      const invalidData = {
        title: 'Test Title'
        // missing url
      };

      expect(() => {
        fileProcessor.validateData(invalidData);
      }).toThrow('Отсутствуют обязательные поля: url');
    });

    test('should throw error for invalid URL', () => {
      const invalidData = {
        url: 'not-a-valid-url',
        title: 'Test Title'
      };

      expect(() => {
        fileProcessor.validateData(invalidData);
      }).toThrow('Некорректный URL');
    });

    test('should add default values for missing optional fields', () => {
      const data = {
        url: 'https://example.com',
        title: 'Test Title'
      };

      fileProcessor.validateData(data);
      
      expect(data.meta_keywords).toBeDefined();
      expect(data.related_keywords).toBeDefined();
      expect(data.main_keyword).toBeDefined();
      expect(data.meta_description).toBeDefined();
    });
  });

  describe('extractKeywordsFromTitle', () => {
    test('should extract keywords from title', () => {
      const title = 'Проверка брачного договора онлайн нейросетью';
      
      const keywords = fileProcessor.extractKeywordsFromTitle(title);
      
      expect(keywords).toContain('проверка');
      expect(keywords).toContain('брачного');
      expect(keywords).toContain('договора');
      expect(keywords.length).toBeLessThanOrEqual(5);
    });

    test('should return default keyword for short titles', () => {
      const title = 'AB';
      
      const keywords = fileProcessor.extractKeywordsFromTitle(title);
      
      expect(keywords).toEqual(['услуги']);
    });
  });

  describe('createExampleFile', () => {
    test('should create valid example file content', () => {
      const example = fileProcessor.createExampleFile();
      
      expect(example).toContain('---');
      expect(example).toContain('url: https://example.com/services');
      expect(example).toContain('title: Профессиональные услуги');
      expect(example).toContain('meta_keywords:');
      expect(example).toContain('Основной текст страницы');
    });
  });

  describe('processFile', () => {
    const testFilesDir = path.join(__dirname, '../fixtures');
    
    beforeAll(async () => {
      await fs.ensureDir(testFilesDir);
    });
    
    afterAll(async () => {
      await fs.remove(testFilesDir);
    });

    test('should process valid YAML file', async () => {
      const testFile = path.join(testFilesDir, 'test.yaml');
      const content = `---
url: https://example.com
title: Test Title
meta_keywords:
  - test
  - yaml
---
Test content`;
      
      await fs.writeFile(testFile, content);
      
      const result = await fileProcessor.processFile(testFile);
      
      expect(result.url).toBe('https://example.com');
      expect(result.title).toBe('Test Title');
      expect(result.meta_keywords).toEqual(['test', 'yaml']);
      
      // Файл должен быть удален после обработки
      expect(await fs.pathExists(testFile)).toBe(false);
    });

    test('should throw error for unsupported file format', async () => {
      const testFile = path.join(testFilesDir, 'test.pdf');
      await fs.writeFile(testFile, 'test content');
      
      await expect(fileProcessor.processFile(testFile)).rejects.toThrow('Неподдерживаемый формат файла');
      
      // Файл должен быть удален даже при ошибке
      expect(await fs.pathExists(testFile)).toBe(false);
    });
  });
});
