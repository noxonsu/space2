const request = require('supertest');
const app = require('../../src/index');
const fs = require('fs-extra');
const path = require('path');

describe('API Integration Tests', () => {
  let server;
  
  beforeAll((done) => {
    server = app.listen(3001, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  describe('Health Check', () => {
    test('GET /api/status should return service status', async () => {
      const response = await request(app)
        .get('/api/status')
        .expect(200);

      expect(response.body).toEqual({
        status: 'ok',
        timestamp: expect.any(String),
        version: '1.0.0'
      });
    });
  });

  describe('Authentication Routes', () => {
    describe('GET /auth/yandex/url', () => {
      test('should return authorization URL', async () => {
        const response = await request(app)
          .get('/auth/yandex/url')
          .expect(200);

        expect(response.body).toHaveProperty('authUrl');
        expect(response.body.authUrl).toContain('oauth.yandex.ru/authorize');
        expect(response.body.authUrl).toContain('client_id=test_client_id');
        expect(response.body.authUrl).toContain('scope=direct:api');
      });
    });

    describe('POST /auth/yandex/validate', () => {
      test('should return error for missing token', async () => {
        const response = await request(app)
          .post('/auth/yandex/validate')
          .send({})
          .expect(400);

        expect(response.body.error).toBe('Токен доступа не предоставлен');
      });

      test('should handle invalid token', async () => {
        const response = await request(app)
          .post('/auth/yandex/validate')
          .send({ access_token: 'invalid_token' })
          .expect(401);

        expect(response.body.valid).toBe(false);
      });
    });
  });

  describe('Campaign Routes', () => {
    const mockToken = 'Bearer test_token';

    describe('GET /api/campaigns', () => {
      test('should require authorization', async () => {
        const response = await request(app)
          .get('/api/campaigns')
          .expect(401);

        expect(response.body.error).toBe('Токен доступа не предоставлен');
      });

      test('should handle authorized request', async () => {
        const response = await request(app)
          .get('/api/campaigns')
          .set('Authorization', mockToken)
          .expect(500); // Ожидаем ошибку, так как используем тестовый токен

        expect(response.body.error).toContain('Не удалось получить список кампаний');
      });
    });

    describe('POST /api/campaigns/generate-ads', () => {
      test('should require page data', async () => {
        const response = await request(app)
          .post('/api/campaigns/generate-ads')
          .set('Authorization', mockToken)
          .send({})
          .expect(400);

        expect(response.body.error).toBe('Данные страницы не предоставлены');
      });

      test('should generate ads with valid data', async () => {
        const pageData = {
          url: 'https://example.com',
          title: 'Test Page',
          meta_description: 'Test description',
          meta_keywords: ['test', 'page'],
          main_keyword: 'test'
        };

        const response = await request(app)
          .post('/api/campaigns/generate-ads')
          .set('Authorization', mockToken)
          .send({ pageData })
          .expect(500); // Ожидаем ошибку OpenAI в тестовой среде

        expect(response.body.error).toContain('Не удалось сгенерировать объявления');
      });
    });

    describe('GET /api/campaigns/example', () => {
      test('should return example data and endpoints', async () => {
        const response = await request(app)
          .get('/api/campaigns/example')
          .expect(200);

        expect(response.body).toHaveProperty('example');
        expect(response.body).toHaveProperty('endpoints');
        expect(response.body.example.pageData).toHaveProperty('url');
        expect(response.body.example.pageData).toHaveProperty('title');
      });
    });
  });

  describe('File Processing', () => {
    const testFilesDir = path.join(__dirname, '../fixtures/integration');

    beforeAll(async () => {
      await fs.ensureDir(testFilesDir);
    });

    afterAll(async () => {
      await fs.remove(testFilesDir);
    });

    test('should process valid YAML file', async () => {
      const testContent = `---
url: https://example.com/test
title: Integration Test File
meta_description: Test file for integration testing
meta_keywords:
  - integration
  - test
  - yaml
main_keyword: integration
---

This is test content for integration testing.`;

      const testFile = path.join(testFilesDir, 'test.yaml');
      await fs.writeFile(testFile, testContent);

      const response = await request(app)
        .post('/api/process-file')
        .set('Authorization', 'Bearer test_token')
        .attach('file', testFile)
        .field('accessToken', 'test_token')
        .expect(500); // Ожидаем ошибку API в тестовой среде

      expect(response.body.error).toContain('Произошла ошибка при обработке файла');
    });

    test('should reject invalid file format', async () => {
      const testFile = path.join(testFilesDir, 'test.pdf');
      await fs.writeFile(testFile, 'Invalid file content');

      const response = await request(app)
        .post('/api/process-file')
        .attach('file', testFile)
        .field('accessToken', 'test_token')
        .expect(400);

      expect(response.body.error).toBe('Неподдерживаемый тип файла');
    });

    test('should require file upload', async () => {
      const response = await request(app)
        .post('/api/process-file')
        .field('accessToken', 'test_token')
        .expect(400);

      expect(response.body.error).toBe('Файл не загружен');
    });

    test('should require access token', async () => {
      const testFile = path.join(testFilesDir, 'test.yaml');
      await fs.writeFile(testFile, 'url: https://example.com\ntitle: Test');

      const response = await request(app)
        .post('/api/process-file')
        .attach('file', testFile)
        .expect(400);

      expect(response.body.error).toBe('Токен доступа не предоставлен');
    });
  });

  describe('Error Handling', () => {
    test('should handle 404 for unknown routes', async () => {
      const response = await request(app)
        .get('/api/unknown-route')
        .expect(404);

      expect(response.body.error).toBe('Эндпоинт не найден');
    });

    test('should handle malformed JSON', async () => {
      const response = await request(app)
        .post('/api/campaigns/generate-ads')
        .set('Authorization', 'Bearer test_token')
        .set('Content-Type', 'application/json')
        .send('{"invalid": json}')
        .expect(400);
    });
  });

  describe('Static Files', () => {
    test('should serve index.html', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.text).toContain('Яндекс.Директ Сервис');
    });
  });
});
