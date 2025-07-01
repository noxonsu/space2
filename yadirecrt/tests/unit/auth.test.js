const request = require('supertest');
const express = require('express');
const authRouter = require('../../src/routes/auth');
const axios = require('axios');

// Mock модулей
jest.mock('axios');
jest.mock('../../src/utils/logger', () => ({
  error: jest.fn(),
  info: jest.fn()
}));

describe('Auth Routes', () => {
  let app;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/auth', authRouter);
    jest.clearAllMocks();

    // Установка переменных окружения для тестов
    process.env.YANDEX_OAUTH_URL = 'https://oauth.yandex.ru';
    process.env.YANDEX_CLIENT_ID = 'test_client_id';
    process.env.YANDEX_REDIRECT_URI = 'http://localhost:3000/auth/yandex/callback';
    process.env.YANDEX_CLIENT_SECRET = 'test_client_secret';
  });

  describe('GET /auth/yandex/url', () => {
    test('should return authorization URL', async () => {
      const response = await request(app)
        .get('/auth/yandex/url')
        .expect(200);

      expect(response.body).toHaveProperty('authUrl');
      expect(response.body).toHaveProperty('message');
      
      const authUrl = response.body.authUrl;
      expect(authUrl).toContain('https://oauth.yandex.ru/authorize');
      expect(authUrl).toContain('client_id=test_client_id');
      expect(authUrl).toContain('response_type=code');
      expect(authUrl).toContain('scope=direct:api');
      expect(authUrl).toContain('redirect_uri=');
    });

    test('should handle missing environment variables', async () => {
      delete process.env.YANDEX_CLIENT_ID;

      const response = await request(app)
        .get('/auth/yandex/url')
        .expect(500);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /auth/yandex/callback', () => {
    test('should handle successful authorization callback', async () => {
      const mockTokenResponse = {
        data: {
          access_token: 'test_access_token',
          refresh_token: 'test_refresh_token',
          token_type: 'Bearer',
          expires_in: 3600
        }
      };

      const mockUserResponse = {
        data: {
          login: 'testuser',
          id: 12345
        }
      };

      axios.post.mockResolvedValueOnce(mockTokenResponse);
      axios.get.mockResolvedValueOnce(mockUserResponse);

      const response = await request(app)
        .get('/auth/yandex/callback?code=test_auth_code')
        .expect(200);

      expect(response.body).toHaveProperty('access_token', 'test_access_token');
      expect(response.body).toHaveProperty('user');
      expect(response.body.user).toHaveProperty('login', 'testuser');

      expect(axios.post).toHaveBeenCalledWith(
        'https://oauth.yandex.ru/token',
        expect.objectContaining({
          grant_type: 'authorization_code',
          code: 'test_auth_code',
          client_id: 'test_client_id',
          client_secret: 'test_client_secret'
        })
      );
    });

    test('should handle authorization error', async () => {
      const response = await request(app)
        .get('/auth/yandex/callback?error=access_denied&error_description=User+denied+access')
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Ошибка авторизации');
      expect(response.body).toHaveProperty('details', 'User denied access');
    });

    test('should handle missing authorization code', async () => {
      const response = await request(app)
        .get('/auth/yandex/callback')
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Код авторизации не получен');
    });

    test('should handle token exchange error', async () => {
      axios.post.mockRejectedValueOnce(new Error('Token exchange failed'));

      const response = await request(app)
        .get('/auth/yandex/callback?code=test_auth_code')
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Ошибка при получении токена');
    });

    test('should handle user info fetch error', async () => {
      const mockTokenResponse = {
        data: {
          access_token: 'test_access_token',
          refresh_token: 'test_refresh_token',
          token_type: 'Bearer',
          expires_in: 3600
        }
      };

      axios.post.mockResolvedValueOnce(mockTokenResponse);
      axios.get.mockRejectedValueOnce(new Error('User info fetch failed'));

      const response = await request(app)
        .get('/auth/yandex/callback?code=test_auth_code')
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Ошибка при получении информации о пользователе');
    });
  });

  describe('POST /auth/refresh', () => {
    test('should refresh access token', async () => {
      const mockRefreshResponse = {
        data: {
          access_token: 'new_access_token',
          refresh_token: 'new_refresh_token',
          token_type: 'Bearer',
          expires_in: 3600
        }
      };

      axios.post.mockResolvedValueOnce(mockRefreshResponse);

      const response = await request(app)
        .post('/auth/refresh')
        .send({ refresh_token: 'old_refresh_token' })
        .expect(200);

      expect(response.body).toHaveProperty('access_token', 'new_access_token');
      expect(response.body).toHaveProperty('refresh_token', 'new_refresh_token');

      expect(axios.post).toHaveBeenCalledWith(
        'https://oauth.yandex.ru/token',
        expect.objectContaining({
          grant_type: 'refresh_token',
          refresh_token: 'old_refresh_token',
          client_id: 'test_client_id',
          client_secret: 'test_client_secret'
        })
      );
    });

    test('should handle missing refresh token', async () => {
      const response = await request(app)
        .post('/auth/refresh')
        .send({})
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Refresh token не предоставлен');
    });

    test('should handle refresh token error', async () => {
      axios.post.mockRejectedValueOnce(new Error('Refresh failed'));

      const response = await request(app)
        .post('/auth/refresh')
        .send({ refresh_token: 'invalid_token' })
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Ошибка при обновлении токена');
    });
  });
});
