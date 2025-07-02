const OpenAIService = require('../../src/services/openaiService');

// Мокаем OpenAI SDK
jest.mock('openai', () => {
  return jest.fn().mockImplementation(() => ({
    chat: {
      completions: {
        create: jest.fn()
      }
    }
  }));
});

describe('OpenAIService', () => {
  let openaiService;
  let mockOpenAI;

  beforeEach(() => {
    jest.clearAllMocks();
    openaiService = new OpenAIService();
    mockOpenAI = openaiService.openai;
  });

  describe('constructor', () => {
    test('should initialize OpenAI client', () => {
      expect(openaiService.openai).toBeDefined();
    });
  });

  describe('generateAds', () => {
    const testPageData = {
      url: 'https://example.com',
      title: 'Test Title',
      meta_description: 'Test description',
      meta_keywords: ['keyword1', 'keyword2'],
      related_keywords: ['related1', 'related2'],
      main_keyword: 'keyword1'
    };

    test('should generate ads successfully', async () => {
      const mockResponse = {
        choices: [{
          message: {
            content: JSON.stringify({
              ads: [
                {
                  title: 'Test Ad Title',
                  title2: 'Subtitle',
                  description: 'Test ad description'
                }
              ]
            })
          }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await openaiService.generateAds(testPageData);

      expect(result).toHaveLength(1);
      expect(result[0]).toEqual({
        title: 'Test Ad Title',
        title2: 'Subtitle',
        description: 'Test ad description',
        url: testPageData.url
      });

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-4',
        messages: expect.any(Array),
        temperature: 0.7,
        max_tokens: 1500
      });
    });

    test('should handle non-JSON response format', async () => {
      const mockResponse = {
        choices: [{
          message: {
            content: `
Заголовок: Test Title
Описание: Test Description
            `
          }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await openaiService.generateAds(testPageData);

      expect(result).toHaveLength(1);
      expect(result[0].url).toBe(testPageData.url);
    });

    test('should return fallback ad on parsing error', async () => {
      const mockResponse = {
        choices: [{
          message: {
            content: 'Invalid response format'
          }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await openaiService.generateAds(testPageData);

      expect(result).toHaveLength(1);
      expect(result[0]).toEqual({
        title: 'Профессиональные услуги',
        title2: 'Онлайн консультация',
        description: 'Получите профессиональную помощь. Быстро и надежно!',
        url: testPageData.url,
        displayPath: 'services'
      });
    });

    test('should throw error on OpenAI API failure', async () => {
      mockOpenAI.chat.completions.create.mockRejectedValue(new Error('API Error'));

      await expect(openaiService.generateAds(testPageData)).rejects.toThrow('Не удалось сгенерировать объявления: API Error');
    });
  });

  describe('buildPrompt', () => {
    test('should build proper prompt for ad generation', () => {
      const testData = {
        url: 'https://example.com',
        title: 'Test Title',
        meta_description: 'Test description',
        meta_keywords: ['keyword1', 'keyword2'],
        related_keywords: ['related1'],
        main_keyword: 'keyword1'
      };

      const prompt = openaiService.buildPrompt(testData);

      expect(prompt).toContain('URL: https://example.com');
      expect(prompt).toContain('Заголовок страницы: Test Title');
      expect(prompt).toContain('Описание: Test description');
      expect(prompt).toContain('Основное ключевое слово: keyword1');
      expect(prompt).toContain('- keyword1');
      expect(prompt).toContain('- keyword2');
      expect(prompt).toContain('- related1');
    });
  });

  describe('parseTextFormat', () => {
    test('should parse text format response', () => {
      const content = `
Заголовок: Test Title
Второй заголовок: Subtitle
Описание: Test Description

Заголовок: Second Ad Title
Описание: Second Description
      `;

      const result = openaiService.parseTextFormat(content, 'https://example.com');

      expect(result).toHaveLength(2);
      expect(result[0]).toEqual({
        title: 'Test Title',
        title2: 'Subtitle',
        description: 'Test Description',
        url: 'https://example.com'
      });
      expect(result[1]).toEqual({
        title: 'Second Ad Title',
        description: 'Second Description',
        url: 'https://example.com'
      });
    });

    test('should return fallback for empty content', () => {
      const result = openaiService.parseTextFormat('', 'https://example.com');

      expect(result).toHaveLength(1);
      expect(result[0].title).toBe('Качественные услуги');
    });
  });

  describe('generateKeywords', () => {
    test('should generate additional keywords', async () => {
      const mockResponse = {
        choices: [{
          message: {
            content: 'новое ключевое слово\nдругое ключевое слово\nтретье ключевое слово'
          }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const testData = {
        title: 'Test Title',
        meta_description: 'Test description',
        meta_keywords: ['existing'],
        related_keywords: ['related'],
        main_keyword: 'main'
      };

      const result = await openaiService.generateKeywords(testData);

      expect(result).toEqual([
        'новое ключевое слово',
        'другое ключевое слово',
        'третье ключевое слово'
      ]);

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-3.5-turbo',
        messages: expect.any(Array),
        temperature: 0.5,
        max_tokens: 500
      });
    });

    test('should return empty array on error', async () => {
      mockOpenAI.chat.completions.create.mockRejectedValue(new Error('API Error'));

      const testData = {
        title: 'Test Title',
        meta_description: 'Test description',
        meta_keywords: [],
        related_keywords: [],
        main_keyword: 'main'
      };

      const result = await openaiService.generateKeywords(testData);

      expect(result).toEqual([]);
    });
  });

  describe('optimizeAd', () => {
    test('should optimize ad based on performance data', async () => {
      const mockResponse = {
        choices: [{
          message: {
            content: 'Рекомендации по оптимизации: увеличить призыв к действию'
          }
        }]
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const adData = {
        title: 'Test Title',
        description: 'Test Description'
      };

      const performance = {
        impressions: 1000,
        clicks: 50,
        ctr: 5.0,
        cpc: 10.5
      };

      const result = await openaiService.optimizeAd(adData, performance);

      expect(result).toBe('Рекомендации по оптимизации: увеличить призыв к действию');

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-4',
        messages: expect.any(Array),
        temperature: 0.6,
        max_tokens: 800
      });
    });

    test('should throw error on optimization failure', async () => {
      mockOpenAI.chat.completions.create.mockRejectedValue(new Error('API Error'));

      const adData = { title: 'Test', description: 'Test' };
      const performance = { impressions: 100, clicks: 5, ctr: 5, cpc: 10 };

      await expect(openaiService.optimizeAd(adData, performance)).rejects.toThrow('API Error');
    });
  });
});
