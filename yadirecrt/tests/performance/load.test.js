const request = require('supertest');
const app = require('../../src/index');
const YandexDirectService = require('../../src/services/yandexDirectService');
const OpenAIService = require('../../src/services/openaiService');

jest.mock('../../src/services/yandexDirectService');
jest.mock('../../src/services/openaiService');

describe('Performance and Load Tests', () => {
  let server;

  beforeAll((done) => {
    server = app.listen(3004, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Базовые моки для всех тестов
    YandexDirectService.mockImplementation(() => ({
      getCampaigns: jest.fn().mockResolvedValue({ Campaigns: [] }),
      createCampaign: jest.fn().mockResolvedValue({ AddResults: [{ Id: 123 }] }),
      createAds: jest.fn().mockResolvedValue({ AddResults: [{ Id: 456 }] })
    }));

    OpenAIService.mockImplementation(() => ({
      generateAds: jest.fn().mockResolvedValue([
        { Title: 'Test Ad', Text: 'Test Text', DisplayUrl: 'example.com' }
      ])
    }));
  });

  describe('Response Time Tests', () => {
    test('should respond to health check within 100ms', async () => {
      const startTime = Date.now();
      
      await request(app)
        .get('/api/status')
        .expect(200);

      const responseTime = Date.now() - startTime;
      expect(responseTime).toBeLessThan(100);
    });

    test('should respond to campaigns list within 2 seconds', async () => {
      const startTime = Date.now();
      
      await request(app)
        .get('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(200);

      const responseTime = Date.now() - startTime;
      expect(responseTime).toBeLessThan(2000);
    });

    test('should handle ad generation within 5 seconds', async () => {
      const startTime = Date.now();
      
      await request(app)
        .post('/api/generate-ads')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'https://example.com',
            title: 'Test Product',
            meta_description: 'Test Description'
          }
        })
        .expect(200);

      const responseTime = Date.now() - startTime;
      expect(responseTime).toBeLessThan(5000);
    }, 10000);
  });

  describe('Concurrent Request Tests', () => {
    test('should handle 10 concurrent campaign requests', async () => {
      const requests = Array(10).fill().map(() =>
        request(app)
          .get('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
      );

      const startTime = Date.now();
      const responses = await Promise.all(requests);
      const totalTime = Date.now() - startTime;

      responses.forEach(response => {
        expect(response.status).toBe(200);
      });

      // Все 10 запросов должны завершиться менее чем за 3 секунды
      expect(totalTime).toBeLessThan(3000);
    });

    test('should handle concurrent campaign creation requests', async () => {
      const pageData = {
        url: 'https://example.com',
        title: 'Test Product',
        meta_description: 'Test Description'
      };

      const requests = Array(5).fill().map((_, index) =>
        request(app)
          .post('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
          .send({
            pageData: { ...pageData, title: `Test Product ${index}` },
            generateAds: false
          })
      );

      const responses = await Promise.all(requests);

      responses.forEach(response => {
        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('success', true);
      });
    });

    test('should handle mixed request types concurrently', async () => {
      const requests = [
        // Health checks
        ...Array(5).fill().map(() => request(app).get('/api/status')),
        
        // Campaign lists
        ...Array(3).fill().map(() => 
          request(app)
            .get('/api/campaigns')
            .set('Authorization', 'Bearer valid_token')
        ),
        
        // Ad generation
        ...Array(2).fill().map(() =>
          request(app)
            .post('/api/generate-ads')
            .set('Authorization', 'Bearer valid_token')
            .send({
              pageData: {
                url: 'https://example.com',
                title: 'Test Product'
              }
            })
        )
      ];

      const responses = await Promise.all(requests);

      responses.forEach(response => {
        expect(response.status).toBeGreaterThanOrEqual(200);
        expect(response.status).toBeLessThan(500);
      });
    });
  });

  describe('Memory and Resource Tests', () => {
    test('should handle large payload requests', async () => {
      const largeContent = 'A'.repeat(50000); // 50KB of content
      const largeKeywords = Array(100).fill().map((_, i) => `keyword${i}`);

      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({
          pageData: {
            url: 'https://example.com',
            title: 'Large Content Test',
            meta_description: 'Test with large content',
            content: largeContent,
            meta_keywords: largeKeywords
          },
          generateAds: false
        })
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
    });

    test('should handle multiple large requests sequentially', async () => {
      const largePageData = {
        url: 'https://example.com',
        title: 'Large Content Test',
        meta_description: 'B'.repeat(10000),
        content: 'C'.repeat(100000),
        meta_keywords: Array(50).fill().map((_, i) => `keyword${i}`)
      };

      for (let i = 0; i < 5; i++) {
        const response = await request(app)
          .post('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
          .send({
            pageData: { ...largePageData, title: `Large Test ${i}` },
            generateAds: false
          });

        expect(response.status).toBe(200);
      }
    });
  });

  describe('Error Handling Under Load', () => {
    test('should maintain error handling under concurrent load', async () => {
      // Настройка мока для генерации ошибок
      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockImplementation(() => {
          // Случайно генерируем ошибки в 30% случаев
          if (Math.random() < 0.3) {
            throw new Error('Simulated API error');
          }
          return Promise.resolve({ Campaigns: [] });
        })
      }));

      const requests = Array(20).fill().map(() =>
        request(app)
          .get('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
      );

      const responses = await Promise.all(requests.map(req => 
        req.then(res => res).catch(err => err.response || err)
      ));

      let successCount = 0;
      let errorCount = 0;

      responses.forEach(response => {
        if (response.status === 200) {
          successCount++;
        } else if (response.status === 500) {
          errorCount++;
          expect(response.body).toHaveProperty('error');
        }
      });

      // Проверяем, что сервер корректно обработал и успешные, и ошибочные запросы
      expect(successCount + errorCount).toBe(20);
      expect(errorCount).toBeGreaterThan(0); // Должны быть ошибки из-за нашего мока
    });

    test('should handle timeout scenarios gracefully', async () => {
      // Mock медленного сервиса
      YandexDirectService.mockImplementation(() => ({
        getCampaigns: jest.fn().mockImplementation(() => 
          new Promise((resolve) => {
            setTimeout(() => resolve({ Campaigns: [] }), 3000);
          })
        )
      }));

      const startTime = Date.now();
      
      const response = await request(app)
        .get('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .timeout(5000);

      const responseTime = Date.now() - startTime;

      expect(response.status).toBe(200);
      expect(responseTime).toBeGreaterThan(2900);
      expect(responseTime).toBeLessThan(5000);
    }, 10000);
  });

  describe('Rate Limiting Tests', () => {
    test('should handle rapid successive requests', async () => {
      const rapidRequests = [];
      
      // Отправляем 50 запросов с минимальной задержкой
      for (let i = 0; i < 50; i++) {
        rapidRequests.push(
          request(app)
            .get('/api/status')
            .then(res => res.status)
            .catch(err => err.status || 500)
        );
        
        // Минимальная задержка между запросами
        await new Promise(resolve => setTimeout(resolve, 10));
      }

      const statuses = await Promise.all(rapidRequests);
      
      // Проверяем, что большинство запросов обработано успешно
      const successCount = statuses.filter(status => status === 200).length;
      expect(successCount).toBeGreaterThan(40); // Минимум 80% успешных
    });

    test('should maintain performance with burst traffic', async () => {
      const burstRequests = [];
      
      // Генерируем пакет из 20 одновременных запросов
      for (let i = 0; i < 20; i++) {
        burstRequests.push(
          request(app)
            .get('/api/campaigns')
            .set('Authorization', 'Bearer valid_token')
        );
      }

      const startTime = Date.now();
      const responses = await Promise.all(burstRequests);
      const totalTime = Date.now() - startTime;

      responses.forEach(response => {
        expect(response.status).toBe(200);
      });

      // Burst должен обрабатываться в разумное время
      expect(totalTime).toBeLessThan(5000);
    });
  });

  describe('Stress Test Scenarios', () => {
    test('should survive extended operation', async () => {
      const iterations = 100;
      let successCount = 0;
      let errorCount = 0;

      for (let i = 0; i < iterations; i++) {
        try {
          const response = await request(app)
            .get('/api/status')
            .timeout(1000);

          if (response.status === 200) {
            successCount++;
          }
        } catch (error) {
          errorCount++;
        }

        // Небольшая пауза между итерациями
        if (i % 10 === 0) {
          await new Promise(resolve => setTimeout(resolve, 50));
        }
      }

      // Проверяем стабильность работы
      expect(successCount).toBeGreaterThan(iterations * 0.95); // 95% успешности
      expect(errorCount).toBeLessThan(iterations * 0.05);
    }, 30000); // Увеличенный timeout для длительного теста
  });
});
