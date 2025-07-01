const request = require('supertest');
const app = require('../../src/index');

describe('Security Tests', () => {
  let server;

  beforeAll((done) => {
    server = app.listen(3005, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  describe('Authentication Security', () => {
    test('should reject requests without authorization header', async () => {
      const protectedEndpoints = [
        '/api/campaigns',
        '/api/campaigns/123/ads',
        '/api/generate-ads',
        '/api/upload'
      ];

      for (const endpoint of protectedEndpoints) {
        const response = await request(app)
          .get(endpoint)
          .expect(401);

        expect(response.body).toHaveProperty('error');
      }
    });

    test('should reject requests with malformed Bearer tokens', async () => {
      const invalidTokens = [
        'Bearer',
        'Bearer ',
        'Basic dGVzdDp0ZXN0',
        'InvalidFormat token',
        'Bearer invalid..token',
        'Bearer ' + 'a'.repeat(1000) // Очень длинный токен
      ];

      for (const token of invalidTokens) {
        const response = await request(app)
          .get('/api/campaigns')
          .set('Authorization', token)
          .expect(401);

        expect(response.body).toHaveProperty('error');
      }
    });

    test('should handle special characters in authorization header', async () => {
      const specialCharTokens = [
        'Bearer <script>alert("xss")</script>',
        'Bearer \'; DROP TABLE users; --',
        'Bearer ../../../etc/passwd',
        'Bearer ${process.env.SECRET_KEY}'
      ];

      for (const token of specialCharTokens) {
        const response = await request(app)
          .get('/api/campaigns')
          .set('Authorization', token)
          .expect(401);

        expect(response.body).toHaveProperty('error');
      }
    });
  });

  describe('Input Validation Security', () => {
    test('should sanitize SQL injection attempts', async () => {
      const sqlInjectionPayloads = [
        "'; DROP TABLE campaigns; --",
        "' OR '1'='1",
        "'; SELECT * FROM users; --",
        "1' UNION SELECT * FROM passwords--"
      ];

      for (const payload of sqlInjectionPayloads) {
        const response = await request(app)
          .get(`/api/campaigns/${payload}/ads`)
          .set('Authorization', 'Bearer valid_token')
          .expect(400);

        expect(response.body).toHaveProperty('error');
      }
    });

    test('should prevent XSS in request data', async () => {
      const xssPayloads = [
        '<script>alert("xss")</script>',
        'javascript:alert("xss")',
        '<img src="x" onerror="alert(1)">',
        '"><script>alert(document.cookie)</script>'
      ];

      for (const payload of xssPayloads) {
        const response = await request(app)
          .post('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
          .send({
            pageData: {
              url: 'https://example.com',
              title: payload,
              meta_description: 'Test'
            }
          });

        // Сервер должен либо отклонить запрос, либо санитизировать данные
        if (response.status === 200) {
          expect(response.body.pageData?.title).not.toContain('<script>');
        }
      }
    });

    test('should validate and sanitize URL inputs', async () => {
      const maliciousUrls = [
        'javascript:alert("xss")',
        'data:text/html,<script>alert(1)</script>',
        'file:///etc/passwd',
        'ftp://malicious.com/backdoor',
        'http://192.168.1.1:22', // Попытка обращения к внутренней сети
        'https://example.com/../../../admin'
      ];

      for (const url of maliciousUrls) {
        const response = await request(app)
          .post('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
          .send({
            pageData: {
              url: url,
              title: 'Test',
              meta_description: 'Test'
            }
          })
          .expect(400);

        expect(response.body).toHaveProperty('error');
      }
    });

    test('should prevent path traversal in file operations', async () => {
      const pathTraversalPayloads = [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\config\\sam',
        '/etc/shadow',
        'C:\\Windows\\System32\\drivers\\etc\\hosts',
        '....//....//....//etc//passwd'
      ];

      for (const payload of pathTraversalPayloads) {
        const response = await request(app)
          .post('/api/upload')
          .set('Authorization', 'Bearer valid_token')
          .attach('file', Buffer.from('test content'), payload);

        // Должен быть отклонен как небезопасный файл
        expect(response.status).toBeGreaterThanOrEqual(400);
      }
    });
  });

  describe('Request Size and Rate Limiting', () => {
    test('should reject oversized payloads', async () => {
      const oversizedPayload = {
        pageData: {
          url: 'https://example.com',
          title: 'A'.repeat(100000), // 100KB заголовок
          meta_description: 'B'.repeat(100000),
          content: 'C'.repeat(1000000), // 1MB контента
          meta_keywords: Array(10000).fill().map((_, i) => `keyword${i}`)
        }
      };

      const response = await request(app)
        .post('/api/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send(oversizedPayload);

      // Сервер должен отклонить слишком большие payloads
      expect(response.status).toBeGreaterThanOrEqual(400);
    }, 10000);

    test('should handle malformed JSON gracefully', async () => {
      const malformedJsons = [
        '{"incomplete": json',
        '{invalid: json}',
        '{"nested": {"too": {"deep": {"structure": {"with": {"many": {"levels": {}}}}}}}}',
        '["array", "with", null, undefined, {"mixed": types}]'
      ];

      for (const json of malformedJsons) {
        const response = await request(app)
          .post('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
          .set('Content-Type', 'application/json')
          .send(json);

        expect(response.status).toBeGreaterThanOrEqual(400);
      }
    });

    test('should prevent DoS through repeated requests', async () => {
      const rapidRequests = [];
      
      // Генерируем много запросов очень быстро
      for (let i = 0; i < 100; i++) {
        rapidRequests.push(
          request(app)
            .get('/api/status')
            .timeout(5000)
            .then(res => res.status)
            .catch(err => err.status || 500)
        );
      }

      const results = await Promise.all(rapidRequests);
      
      // Сервер должен продолжать работать, но может ограничивать запросы
      const serverErrors = results.filter(status => status >= 500).length;
      expect(serverErrors).toBeLessThan(10); // Не более 10% серверных ошибок
    });
  });

  describe('Header Security', () => {
    test('should handle malicious headers', async () => {
      const maliciousHeaders = {
        'X-Forwarded-For': '127.0.0.1, <script>alert(1)</script>',
        'User-Agent': '"><script>alert(document.cookie)</script>',
        'X-Real-IP': '../../../etc/passwd',
        'Custom-Header': 'value\r\nSet-Cookie: admin=true'
      };

      const response = await request(app)
        .get('/api/status')
        .set(maliciousHeaders)
        .expect(200);

      // Проверяем, что сервер не возвращает вредоносные заголовки
      expect(response.headers).not.toHaveProperty('Set-Cookie');
    });

    test('should validate Content-Type header', async () => {
      const maliciousContentTypes = [
        'application/json; charset=utf-8\r\nX-Injected: header',
        'text/html',
        'application/xml',
        'multipart/form-data; boundary=injection'
      ];

      for (const contentType of maliciousContentTypes) {
        const response = await request(app)
          .post('/api/campaigns')
          .set('Authorization', 'Bearer valid_token')
          .set('Content-Type', contentType)
          .send('{"test": "data"}');

        // Сервер должен правильно обрабатывать только JSON
        if (contentType.includes('application/json')) {
          expect(response.status).toBeLessThan(500);
        } else {
          expect(response.status).toBeGreaterThanOrEqual(400);
        }
      }
    });
  });

  describe('File Upload Security', () => {
    test('should reject dangerous file types', async () => {
      const dangerousFiles = [
        { name: 'malware.exe', content: Buffer.from('MZ'), type: 'application/exe' },
        { name: 'script.js', content: Buffer.from('alert("xss")'), type: 'text/javascript' },
        { name: 'config.php', content: Buffer.from('<?php system($_GET["cmd"]); ?>'), type: 'text/php' },
        { name: 'shell.sh', content: Buffer.from('#!/bin/bash\nrm -rf /'), type: 'text/x-shellscript' }
      ];

      for (const file of dangerousFiles) {
        const response = await request(app)
          .post('/api/upload')
          .set('Authorization', 'Bearer valid_token')
          .attach('file', file.content, file.name);

        expect(response.status).toBeGreaterThanOrEqual(400);
        expect(response.body).toHaveProperty('error');
      }
    });

    test('should validate file size limits', async () => {
      const oversizedFile = Buffer.alloc(10 * 1024 * 1024); // 10MB файл
      
      const response = await request(app)
        .post('/api/upload')
        .set('Authorization', 'Bearer valid_token')
        .attach('file', oversizedFile, 'large.yaml');

      expect(response.status).toBeGreaterThanOrEqual(400);
    });

    test('should sanitize file names', async () => {
      const maliciousFileNames = [
        '../../../etc/passwd',
        'file.yaml\x00.exe',
        'file.yaml\r\n.sh',
        'con.yaml', // Windows reserved name
        'aux.yaml'  // Windows reserved name
      ];

      for (const fileName of maliciousFileNames) {
        const response = await request(app)
          .post('/api/upload')
          .set('Authorization', 'Bearer valid_token')
          .attach('file', Buffer.from('url: https://example.com'), fileName);

        expect(response.status).toBeGreaterThanOrEqual(400);
      }
    });
  });

  describe('Information Disclosure', () => {
    test('should not expose sensitive information in error messages', async () => {
      const response = await request(app)
        .get('/api/nonexistent')
        .expect(404);

      const errorMessage = JSON.stringify(response.body);
      
      // Проверяем, что в ошибках нет чувствительной информации
      expect(errorMessage).not.toMatch(/password|secret|key|token/i);
      expect(errorMessage).not.toMatch(/\/home\/|\/var\/|C:\\/);
      expect(errorMessage).not.toMatch(/node_modules|package\.json/);
    });

    test('should not expose stack traces in production', async () => {
      const originalEnv = process.env.NODE_ENV;
      process.env.NODE_ENV = 'production';

      const response = await request(app)
        .get('/api/campaigns/invalid')
        .set('Authorization', 'Bearer valid_token');

      process.env.NODE_ENV = originalEnv;

      const responseText = JSON.stringify(response.body);
      
      // В продакшене не должно быть stack traces
      expect(responseText).not.toMatch(/at Object\.|at Function\.|at Module\./);
      expect(responseText).not.toMatch(/\/src\/|\.js:\d+:\d+/);
    });

    test('should not expose server information', async () => {
      const response = await request(app)
        .get('/api/status')
        .expect(200);

      // Проверяем, что не раскрываются детали сервера
      expect(response.headers['server']).toBeUndefined();
      expect(response.headers['x-powered-by']).not.toMatch(/Express|Node\.js/);
    });
  });
});
