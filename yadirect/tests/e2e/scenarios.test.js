const request = require('supertest');
const app = require('../../src/index');
const YandexDirectService = require('../../src/services/yandexDirectService');
const OpenAIService = require('../../src/services/openaiService');
const FileProcessor = require('../../src/services/fileProcessor');

jest.mock('../../src/services/yandexDirectService');
jest.mock('../../src/services/openaiService');
jest.mock('../../src/services/fileProcessor');

describe('E2E User Scenarios', () => {
  let server;

  beforeAll((done) => {
    server = app.listen(3003, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Complete Campaign Creation Flow', () => {
    test('should complete full campaign creation from file upload to ads generation', async () => {
      // Настройка моков для полного сценария
      const mockPageData = {
        url: 'https://example.com/product',
        title: 'Лучший продукт 2024',
        meta_description: 'Купите лучший продукт по выгодной цене',
        meta_keywords: ['продукт', 'скидка', 'качество'],
        content: 'Подробное описание продукта с ключевыми словами'
      };

      const mockGeneratedAds = [
        {
          Title: 'Лучший продукт 2024 | Скидки до 50%',
          Text: 'Качественный продукт с гарантией. Быстрая доставка по всей России.',
          DisplayUrl: 'example.com/product'
        },
        {
          Title: 'Продукт премиум качества',
          Text: 'Эксклюзивные предложения только для вас. Закажите сегодня!',
          DisplayUrl: 'example.com/product'
        }
      ];

      const mockCampaignResult = {
        AddResults: [{ Id: 12345, Warnings: [] }]
      };

      const mockAdsResult = {
        AddResults: [
          { Id: 67890, Warnings: [] },
          { Id: 67891, Warnings: [] }
        ]
      };

      // Mock FileProcessor
      FileProcessor.mockImplementation(() => ({
        parseFile: jest.fn().mockResolvedValue(mockPageData)
      }));

      // Mock OpenAIService
      OpenAIService.mockImplementation(() => ({
        generateAds: jest.fn().mockResolvedValue(mockGeneratedAds)
      }));

      // Mock YandexDirectService
      YandexDirectService.mockImplementation(() => ({
        createCampaign: jest.fn().mockResolvedValue(mockCampaignResult),
        createAds: jest.fn().mockResolvedValue(mockAdsResult),
        getCampaigns: jest.fn().mockResolvedValue({ 
          Campaigns: [{ Id: 12345, Name: 'Лучший продукт 2024', Status: 'SERVING' }] 
        }),
        getAds: jest.fn().mockResolvedValue({ 
          Ads: mockGeneratedAds.map((ad, index) => ({ ...ad, Id: 67890 + index }))
        })
      }));

      const validToken = 'Bearer valid_access_token';

      // Шаг 1: Загрузка файла с данными страницы
      const yamlContent = Buffer.from(`
url: ${mockPageData.url}
title: ${mockPageData.title}
meta_description: ${mockPageData.meta_description}
meta_keywords:
  - ${mockPageData.meta_keywords[0]}
  - ${mockPageData.meta_keywords[1]}
  - ${mockPageData.meta_keywords[2]}
---
${mockPageData.content}
`);

      const uploadResponse = await request(app)
        .post('/api/upload')
        .set('Authorization', validToken)
        .attach('file', yamlContent, 'product.yaml')
        .expect(200);

      expect(uploadResponse.body).toHaveProperty('success', true);
      expect(uploadResponse.body).toHaveProperty('pageData');

      // Шаг 2: Создание кампании с автогенерацией объявлений
      const campaignResponse = await request(app)
        .post('/api/campaigns')
        .set('Authorization', validToken)
        .send({
          pageData: mockPageData,
          generateAds: true
        })
        .expect(200);

      expect(campaignResponse.body).toHaveProperty('success', true);
      expect(campaignResponse.body).toHaveProperty('campaignId', 12345);
      expect(campaignResponse.body).toHaveProperty('generatedAds');
      expect(campaignResponse.body.generatedAds).toHaveLength(2);

      // Шаг 3: Проверка созданной кампании
      const campaignsResponse = await request(app)
        .get('/api/campaigns')
        .set('Authorization', validToken)
        .expect(200);

      expect(campaignsResponse.body).toHaveProperty('success', true);
      expect(campaignsResponse.body.campaigns).toHaveLength(1);
      expect(campaignsResponse.body.campaigns[0]).toHaveProperty('Id', 12345);

      // Шаг 4: Получение объявлений кампании
      const adsResponse = await request(app)
        .get('/api/campaigns/12345/ads')
        .set('Authorization', validToken)
        .expect(200);

      expect(adsResponse.body).toHaveProperty('success', true);
      expect(adsResponse.body.ads).toHaveLength(2);

      // Проверяем, что все сервисы были вызваны корректно
      expect(FileProcessor).toHaveBeenCalledTimes(1);
      expect(OpenAIService).toHaveBeenCalledTimes(1);
      expect(YandexDirectService).toHaveBeenCalledTimes(3); // create, getCampaigns, getAds
    });

    test('should handle partial failures in campaign creation flow', async () => {
      const mockPageData = {
        url: 'https://example.com/product',
        title: 'Test Product',
        meta_description: 'Test Description'
      };

      // Mock успешную генерацию объявлений, но неудачное создание кампании
      OpenAIService.mockImplementation(() => ({
        generateAds: jest.fn().mockResolvedValue([
          { Title: 'Test Ad', Text: 'Test Text', DisplayUrl: 'example.com' }
        ])
      }));

      YandexDirectService.mockImplementation(() => ({
        createCampaign: jest.fn().mockRejectedValue(new Error('Budget limit exceeded'))
      }));

      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: mockPageData,
          generateAds: true
        })
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Ошибка при создании кампании');
      expect(response.body.details).toContain('Budget limit exceeded');
    });
  });

  describe('Authorization Flow', () => {
    test('should complete OAuth authorization flow', async () => {
      // Шаг 1: Получение URL авторизации
      const authUrlResponse = await request(app)
        .get('/api/auth/yandex/url')
        .expect(200);

      expect(authUrlResponse.body).toHaveProperty('authUrl');
      expect(authUrlResponse.body.authUrl).toContain('oauth.yandex.ru');

      // Шаг 2: Обработка callback (симуляция)
      // В реальном сценарии пользователь переходит по authUrl и возвращается с кодом
      const mockAxios = require('axios');
      mockAxios.post.mockResolvedValueOnce({
        data: {
          access_token: 'new_access_token',
          refresh_token: 'new_refresh_token',
          expires_in: 3600
        }
      });
      mockAxios.get.mockResolvedValueOnce({
        data: {
          login: 'testuser',
          id: 12345
        }
      });

      const callbackResponse = await request(app)
        .get('/api/auth/yandex/callback?code=auth_code_from_yandex')
        .expect(200);

      expect(callbackResponse.body).toHaveProperty('access_token', 'new_access_token');
      expect(callbackResponse.body).toHaveProperty('user');

      // Шаг 3: Использование полученного токена
      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockResolvedValue({ Campaigns: [] })
      }));

      const campaignsResponse = await request(app)
        .get('/api/campaigns')
        .set('Authorization', 'Bearer new_access_token')
        .expect(200);

      expect(campaignsResponse.body).toHaveProperty('success', true);
    });

    test('should handle token refresh flow', async () => {
      const mockAxios = require('axios');
      
      // Mock успешного обновления токена
      mockAxios.post.mockResolvedValueOnce({
        data: {
          access_token: 'refreshed_access_token',
          refresh_token: 'new_refresh_token',
          expires_in: 3600
        }
      });

      const refreshResponse = await request(app)
        .post('/api/auth/refresh')
        .send({ refresh_token: 'old_refresh_token' })
        .expect(200);

      expect(refreshResponse.body).toHaveProperty('access_token', 'refreshed_access_token');
      expect(refreshResponse.body).toHaveProperty('refresh_token', 'new_refresh_token');
    });
  });

  describe('Error Recovery Scenarios', () => {
    test('should handle network timeouts gracefully', async () => {
      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockImplementation(() => 
          new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Network timeout')), 100)
          )
        )
      }));

      const response = await request(app)
        .get('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(500);

      expect(response.body).toHaveProperty('error');
      expect(response.body.details).toContain('Network timeout');
    });

    test('should handle API rate limiting', async () => {
      YandexDirectService.mockImplementation(() => ({
        createCampaign: jest.fn().mockRejectedValue({
          response: {
            status: 429,
            data: { error: 'Rate limit exceeded' }
          }
        })
      }));

      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'https://example.com',
            title: 'Test'
          }
        })
        .expect(500);

      expect(response.body).toHaveProperty('error');
    });

    test('should handle invalid file uploads gracefully', async () => {
      FileProcessor.mockImplementation(() => ({
        parseFile: jest.fn().mockRejectedValue(new Error('Invalid YAML syntax'))
      }));

      const response = await request(app)
        .post('/api/upload')
        .set('Authorization', 'Bearer valid_token')
        .attach('file', Buffer.from('invalid: yaml: content:'), 'invalid.yaml')
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('Performance Scenarios', () => {
    test('should handle large campaign datasets', async () => {
      const largeCampaignsList = Array(100).fill().map((_, index) => ({
        Id: index + 1,
        Name: `Кампания ${index + 1}`,
        Status: 'SERVING'
      }));

      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockResolvedValue({ 
          Campaigns: largeCampaignsList 
        })
      }));

      const startTime = Date.now();
      
      const response = await request(app)
        .get('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(200);

      const responseTime = Date.now() - startTime;

      expect(response.body.campaigns).toHaveLength(100);
      expect(responseTime).toBeLessThan(5000); // Должно быть быстрее 5 секунд
    });

    test('should handle multiple concurrent ad generations', async () => {
      const mockAds = [
        { Title: 'Ad 1', Text: 'Text 1', DisplayUrl: 'example.com' },
        { Title: 'Ad 2', Text: 'Text 2', DisplayUrl: 'example.com' }
      ];

      OpenAIService.mockImplementation(() => ({
        generateAds: jest.fn().mockImplementation(() => 
          new Promise(resolve => setTimeout(() => resolve(mockAds), 500))
        )
      }));

      const requests = Array(5).fill().map(() =>
        request(app)
          .post('/api/generate-ads')
          .set('Authorization', 'Bearer valid_token')
          .send({
            pageData: {
              url: 'https://example.com',
              title: 'Test Product'
            }
          })
      );

      const responses = await Promise.all(requests);

      responses.forEach(response => {
        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('success', true);
        expect(response.body.ads).toHaveLength(2);
      });
    });
  });
});
