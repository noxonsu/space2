const fs = require('fs-extra');
const yaml = require('yaml');
const path = require('path');
const logger = require('../utils/logger');

class FileProcessor {
  constructor() {
    this.supportedFormats = ['.yaml', '.yml', '.txt', '.md'];
  }

  /**
   * Обработка загруженного файла
   */
  async processFile(filePath) {
    try {
      const ext = path.extname(filePath).toLowerCase();
      const content = await fs.readFile(filePath, 'utf8');

      let parsedData;

      switch (ext) {
        case '.yaml':
        case '.yml':
          parsedData = this.parseYamlFile(content);
          break;
        case '.md':
          parsedData = this.parseMarkdownFile(content);
          break;
        case '.txt':
          parsedData = this.parseTextFile(content);
          break;
        default:
          throw new Error(`Неподдерживаемый формат файла: ${ext}`);
      }

      // Валидация данных
      this.validateData(parsedData);

      // Очистка временного файла
      await fs.remove(filePath);

      logger.info('Файл успешно обработан');
      return parsedData;

    } catch (error) {
      logger.error('Ошибка при обработке файла:', error);
      // Пытаемся удалить временный файл даже при ошибке
      try {
        await fs.remove(filePath);
      } catch (cleanupError) {
        logger.error('Ошибка при очистке временного файла:', cleanupError);
      }
      throw error;
    }
  }

  /**
   * Парсинг YAML файла
   */
  parseYamlFile(content) {
    try {
      // Разделяем frontmatter и контент
      const parts = content.split('---').filter(part => part.trim());
      
      if (parts.length === 0) {
        throw new Error('Файл не содержит данных');
      }

      // Первая часть - YAML frontmatter
      const yamlContent = parts[0];
      const parsed = yaml.parse(yamlContent);

      // Если есть вторая часть - это основной контент
      if (parts.length > 1) {
        parsed.content = parts.slice(1).join('---').trim();
      }

      return parsed;
    } catch (error) {
      throw new Error(`Ошибка парсинга YAML: ${error.message}`);
    }
  }

  /**
   * Парсинг Markdown файла
   */
  parseMarkdownFile(content) {
    try {
      // Проверяем наличие frontmatter
      if (content.startsWith('---')) {
        const endIndex = content.indexOf('---', 3);
        if (endIndex !== -1) {
          const frontmatter = content.substring(3, endIndex).trim();
          const mainContent = content.substring(endIndex + 3).trim();
          
          const parsed = yaml.parse(frontmatter);
          parsed.content = mainContent;
          
          return parsed;
        }
      }

      // Если нет frontmatter, пытаемся извлечь данные из текста
      return this.extractDataFromText(content);
    } catch (error) {
      throw new Error(`Ошибка парсинга Markdown: ${error.message}`);
    }
  }

  /**
   * Парсинг текстового файла
   */
  parseTextFile(content) {
    try {
      // Если файл начинается с YAML frontmatter
      if (content.startsWith('---')) {
        return this.parseMarkdownFile(content);
      }

      // Иначе пытаемся извлечь данные из текста
      return this.extractDataFromText(content);
    } catch (error) {
      throw new Error(`Ошибка парсинга текстового файла: ${error.message}`);
    }
  }

  /**
   * Извлечение данных из простого текста
   */
  extractDataFromText(content) {
    const data = {
      title: '',
      meta_description: '',
      meta_keywords: [],
      related_keywords: [],
      main_keyword: '',
      url: '',
      content: content
    };

    const lines = content.split('\n');

    for (const line of lines) {
      const trimmed = line.trim();
      
      if (trimmed.startsWith('URL:') || trimmed.startsWith('url:')) {
        data.url = trimmed.split(':').slice(1).join(':').trim();
      } else if (trimmed.startsWith('Title:') || trimmed.startsWith('title:')) {
        data.title = trimmed.split(':').slice(1).join(':').trim();
      } else if (trimmed.startsWith('Description:') || trimmed.startsWith('description:')) {
        data.meta_description = trimmed.split(':').slice(1).join(':').trim();
      } else if (trimmed.startsWith('Keywords:') || trimmed.startsWith('keywords:')) {
        const keywordsStr = trimmed.split(':').slice(1).join(':').trim();
        data.meta_keywords = keywordsStr.split(',').map(k => k.trim()).filter(k => k);
      }
    }

    // Если не найдены ключевые данные, пытаемся их сгенерировать
    if (!data.title && lines.length > 0) {
      data.title = lines[0].trim();
    }

    if (!data.meta_description && lines.length > 1) {
      data.meta_description = lines.slice(1, 3).join(' ').trim();
    }

    return data;
  }

  /**
   * Валидация данных
   */
  validateData(data) {
    const required = ['url', 'title'];
    const missing = required.filter(field => !data[field] || data[field].trim() === '');

    if (missing.length > 0) {
      throw new Error(`Отсутствуют обязательные поля: ${missing.join(', ')}`);
    }

    // Валидация URL
    try {
      new URL(data.url);
    } catch (error) {
      throw new Error('Некорректный URL');
    }

    // Проверяем наличие ключевых слов
    if (!data.meta_keywords || !Array.isArray(data.meta_keywords) || data.meta_keywords.length === 0) {
      logger.warn('Ключевые слова не найдены, попытаемся извлечь из заголовка');
      data.meta_keywords = this.extractKeywordsFromTitle(data.title);
    }

    // Проверяем наличие связанных ключевых слов
    if (!data.related_keywords || !Array.isArray(data.related_keywords)) {
      data.related_keywords = [];
    }

    // Устанавливаем основное ключевое слово если не указано
    if (!data.main_keyword && data.meta_keywords.length > 0) {
      data.main_keyword = data.meta_keywords[0];
    }

    // Проверяем наличие описания
    if (!data.meta_description || data.meta_description.trim() === '') {
      logger.warn('Описание не найдено, будет использовано значение по умолчанию');
      data.meta_description = `Профессиональные услуги по ${data.main_keyword}. Качественно и надежно.`;
    }
  }

  /**
   * Извлечение ключевых слов из заголовка
   */
  extractKeywordsFromTitle(title) {
    // Простое извлечение ключевых слов из заголовка
    const words = title.toLowerCase()
      .replace(/[^\wа-яё\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2)
      .slice(0, 5);

    return words.length > 0 ? words : ['услуги'];
  }

  /**
   * Создание примера файла
   */
  createExampleFile() {
    const example = {
      url: 'https://example.com/services',
      title: 'Профессиональные услуги',
      meta_description: 'Качественные профессиональные услуги с гарантией результата',
      meta_keywords: [
        'профессиональные услуги',
        'качественные услуги',
        'надежные услуги'
      ],
      related_keywords: [
        'консультация специалиста',
        'профессиональная помощь',
        'экспертные услуги'
      ],
      main_keyword: 'профессиональные услуги',
      content: 'Основной текст страницы с описанием услуг...'
    };

    return `---
${yaml.stringify(example)}---

${example.content}`;
  }
}

module.exports = FileProcessor;
