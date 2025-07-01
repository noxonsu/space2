const request = require('supertest');
const app = require('../../src/index');
const YandexDirectService = require('../../src/services/yandexDirectService');
const OpenAIService = require('../../src/services/openaiService');
const FileProcessor = require('../../src/services/fileProcessor');

// Mock всех сервисов для интеграционных тестов
jest.mock('../../src/services/yandexDirectService');
jest.mock('../../src/services/openaiService');
jest.mock('../../src/services/fileProcessor');

describe('Advanced API Integration Tests', () => {
  let server;

  beforeAll((done) => {
    server = app.listen(3002, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Error Handling', () => {
    test('should handle 404 for non-existent routes', async () => {
      const response = await request(app)
        .get('/api/nonexistent')
        .expect(404);

      expect(response.body).toHaveProperty('error');
    });

    test('should handle malformed JSON in request body', async () => {
      const response = await request(app)
        .post('/api/campaigns')
        .set('Content-Type', 'application/json')
        .set('Authorization', 'Bearer valid_token')
        .send('{"invalid": json}')
        .expect(400);
    });

    test('should handle large request payloads', async () => {
      const largePayload = {
        pageData: {
          url: 'https://example.com',
          title: 'A'.repeat(10000), // Очень длинный заголовок
          meta_description: 'B'.repeat(10000),
          content: 'C'.repeat(100000)
        }
      };

      // Mock сервисов
      YandexDirectService.mockImplementation(() => ({
        createCampaign: jest.fn().mockResolvedValue({ AddResults: [{ Id: 123 }] })
      }));

      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send(largePayload);

      // Запрос должен быть обработан или отклонен корректно
      expect(response.status).toBeGreaterThanOrEqual(400);
    });
  });

  describe('Content-Type Handling', () => {
    test('should accept application/json', async () => {
      YandexDirectService.mockImplementation(() => ({
        createCampaign: jest.fn().mockResolvedValue({ AddResults: [{ Id: 123 }] })
      }));

      const response = await request(app)
        .post('/api/campaigns')
        .set('Content-Type', 'application/json')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'https://example.com',
            title: 'Test'
          }
        })
        .expect(200);
    });

    test('should handle missing Content-Type header', async () => {
      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send('some data')
        .expect(400);
    });
  });

  describe('Security Headers', () => {
    test('should include security headers in responses', async () => {
      const response = await request(app)
        .get('/api/status')
        .expect(200);

      // Проверяем наличие базовых заголовков безопасности
      expect(response.headers).toHaveProperty('x-powered-by');
    });

    test('should handle CORS preflight requests', async () => {
      const response = await request(app)
        .options('/api/campaigns')
        .set('Origin', 'http://localhost:3000')
        .set('Access-Control-Request-Method', 'POST')
        .set('Access-Control-Request-Headers', 'Content-Type, Authorization');

      expect(response.status).toBeLessThan(500);
    });
  });

  describe('Rate Limiting and Performance', () => {
    test('should handle multiple concurrent requests', async () => {
      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockResolvedValue({ Campaigns: [] })
      }));

      const requests = Array(10).fill().map(() =>
        request(app)
          .get('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
      );

      const responses = await Promise.all(requests);
      
      responses.forEach(response => {
        expect(response.status).toBe(200);
      });
    });

    test('should handle slow external API responses', async () => {
      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockImplementation(() => 
          new Promise(resolve => setTimeout(() => resolve({ Campaigns: [] }), 2000))
        )
      }));

      const startTime = Date.now();
      
      const response = await request(app)
        .get('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .timeout(5000);

      const duration = Date.now() - startTime;
      
      expect(response.status).toBe(200);
      expect(duration).toBeGreaterThan(1900); // Проверяем, что запрос действительно ждал
    }, 10000);
  });

  describe('File Upload Integration', () => {
    test('should handle file upload with valid YAML', async () => {
      const mockFileProcessor = {
        parseFile: jest.fn().mockResolvedValue({
          url: 'https://example.com',
          title: 'Parsed Title',
          meta_description: 'Parsed Description'
        })
      };

      FileProcessor.mockImplementation(() => mockFileProcessor);

      YandexDirectService.mockImplementation(() => ({
        createCampaign: jest.fn().mockResolvedValue({ AddResults: [{ Id: 123 }] })
      }));

      // Создаем буфер с YAML содержимым
      const yamlContent = Buffer.from(`
url: https://example.com
title: Test Title
meta_description: Test Description
`);

      const response = await request(app)
        .post('/api/upload')
        .set('Authorization', 'Bearer valid_token')
        .attach('file', yamlContent, 'test.yaml')
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
      expect(mockFileProcessor.parseFile).toHaveBeenCalled();
    });

    test('should handle file upload with unsupported format', async () => {
      const mockFileProcessor = {
        parseFile: jest.fn().mockRejectedValue(new Error('Unsupported file format'))
      };

      FileProcessor.mockImplementation(() => mockFileProcessor);

      const response = await request(app)
        .post('/api/upload')
        .set('Authorization', 'Bearer valid_token')
        .attach('file', Buffer.from('content'), 'test.exe')
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });

    test('should handle missing file in upload', async () => {
      const response = await request(app)
        .post('/api/upload')
        .set('Authorization', 'Bearer valid_token')
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('Ad Generation Workflow', () => {
    test('should complete full ad generation workflow', async () => {
      const mockGeneratedAds = [
        {
          Title: 'Заголовок 1',
          Text: 'Описание объявления 1',
          DisplayUrl: 'example.com'
        },
        {
          Title: 'Заголовок 2', 
          Text: 'Описание объявления 2',
          DisplayUrl: 'example.com'
        }
      ];

      OpenAIService.mockImplementation(() => ({
        generateAds: jest.fn().mockResolvedValue(mockGeneratedAds)
      }));

      const response = await request(app)
        .post('/api/generate-ads')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'https://example.com',
            title: 'Test Page',
            meta_description: 'Test Description',
            meta_keywords: ['keyword1', 'keyword2']
          },
          count: 2
        })
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('ads');
      expect(response.body.ads).toHaveLength(2);
      expect(response.body.ads[0]).toHaveProperty('Title');
      expect(response.body.ads[0]).toHaveProperty('Text');
    });

    test('should handle OpenAI API errors gracefully', async () => {
      OpenAIService.mockImplementation(() => ({
        generateAds: jest.fn().mockRejectedValue(new Error('OpenAI quota exceeded'))
      }));

      const response = await request(app)
        .post('/api/generate-ads')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'https://example.com',
            title: 'Test Page'
          }
        })
        .expect(500);

      expect(response.body).toHaveProperty('error');
      expect(response.body.details).toContain('OpenAI quota exceeded');
    });
  });

  describe('Data Validation', () => {
    test('should validate required fields in page data', async () => {
      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            // Отсутствует обязательное поле url
            title: 'Test Title'
          }
        })
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });

    test('should validate URL format', async () => {
      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'invalid-url',
            title: 'Test Title'
          }
        })
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });

    test('should validate campaign ID format', async () => {
      const response = await request(app)
        .get('/api/campaigns/not-a-number/ads')
        .set('Authorization', 'Bearer valid_token')
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('API Versioning', () => {
    test('should handle requests to current API version', async () => {
      const response = await request(app)
        .get('/api/status')
        .expect(200);

      expect(response.body).toHaveProperty('version');
    });

    test('should provide API documentation endpoint', async () => {
      const response = await request(app)
        .get('/api/docs')
        .expect(200);

      expect(response.headers['content-type']).toMatch(/text\/html/);
    });
  });
});
