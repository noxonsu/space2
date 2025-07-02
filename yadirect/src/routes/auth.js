const express = require('express');
const axios = require('axios');
const logger = require('../utils/logger');

const router = express.Router();

/**
 * Получение URL для авторизации в Яндексе
 */
router.get('/yandex/url', (req, res) => {
  try {
    if (!process.env.YANDEX_CLIENT_ID || !process.env.YANDEX_OAUTH_URL || !process.env.YANDEX_REDIRECT_URI) {
      throw new Error('Не хватает необходимых переменных окружения');
    }

    const authUrl = `${process.env.YANDEX_OAUTH_URL}/authorize?` +
      `response_type=code&` +
      `client_id=${process.env.YANDEX_CLIENT_ID}&` +
      `redirect_uri=${encodeURIComponent(process.env.YANDEX_REDIRECT_URI)}&` +
      `scope=direct:api&` +
      `state=${Date.now()}`;

    res.json({ 
      authUrl,
      message: 'Перейдите по ссылке для авторизации в Яндексе'
    });
  } catch (error) {
    logger.error('Ошибка при генерации URL авторизации:', error);
    res.status(500).json({ error: 'Не удалось сгенерировать URL авторизации' });
  }
});

/**
 * Обработка колбэка от Яндекса
 */
router.get('/yandex/callback', async (req, res) => {
  try {
    const { code, error, error_description } = req.query;

    if (error) {
      logger.error('Ошибка авторизации Яндекс:', error_description);
      return res.status(400).json({ 
        error: 'Ошибка авторизации',
        details: error_description 
      });
    }

    if (!code) {
      return res.status(400).json({ error: 'Код авторизации не получен' });
    }

    // Обмениваем код на токен
    const tokenResponse = await axios.post(`${process.env.YANDEX_OAUTH_URL}/token`, {
      grant_type: 'authorization_code',
      code: code,
      client_id: process.env.YANDEX_CLIENT_ID,
      client_secret: process.env.YANDEX_CLIENT_SECRET,
      redirect_uri: process.env.YANDEX_REDIRECT_URI
    });

    const { access_token, expires_in, refresh_token } = tokenResponse.data;

    if (!access_token) {
      throw new Error('Токен доступа не получен');
    }

    logger.info('Успешная авторизация в Яндекс.Директ');

    // Получаем информацию о пользователе
    try {
      const userResponse = await axios.get(`${process.env.YANDEX_OAUTH_URL}/info`, {
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      });

      // В реальном приложении здесь бы сохраняли токен в БД или сессии
      res.json({
        success: true,
        access_token,
        expires_in,
        refresh_token,
        user: userResponse.data,
        message: 'Авторизация успешно завершена'
      });
    } catch (userError) {
      logger.error('Ошибка при получении информации о пользователе:', userError);
      return res.status(500).json({ 
        error: 'Ошибка при получении информации о пользователе',
        details: userError.message 
      });
    }

  } catch (error) {
    logger.error('Ошибка при обработке колбэка:', error);
    res.status(500).json({ 
      error: 'Ошибка при получении токена',
      details: error.message 
    });
  }
});

/**
 * POST /auth/refresh
 * Обновление токена доступа
 */
router.post('/refresh', async (req, res) => {
  try {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      return res.status(400).json({ error: 'Refresh token не предоставлен' });
    }

    // Обновление токена через Яндекс OAuth
    const response = await axios.post('https://oauth.yandex.ru/token', {
      grant_type: 'refresh_token',
      refresh_token: refresh_token,
      client_id: process.env.YANDEX_CLIENT_ID,
      client_secret: process.env.YANDEX_CLIENT_SECRET
    });

    res.json({
      access_token: response.data.access_token,
      refresh_token: response.data.refresh_token,
      expires_in: response.data.expires_in,
      message: 'Токен успешно обновлен'
    });

  } catch (error) {
    logger.error('Ошибка при обновлении токена:', error);
    res.status(500).json({ 
      error: 'Ошибка при обновлении токена',
      details: error.message 
    });
  }
});

/**
 * POST /auth/yandex/validate
 * Валидация токена Яндекс.Директ
 */
router.post('/yandex/validate', async (req, res) => {
  try {
    const { access_token } = req.body;

    if (!access_token) {
      return res.status(400).json({ 
        valid: false,
        error: 'Токен не предоставлен' 
      });
    }

    // Проверка токена через API Яндекс.Директ
    const yandexDirect = new (require('../services/yandexDirectService'))(access_token);
    
    try {
      await yandexDirect.validateToken();
      res.json({
        valid: true,
        message: 'Токен действителен'
      });
    } catch (validationError) {
      res.status(401).json({
        valid: false,
        error: 'Токен недействителен',
        details: validationError.message
      });
    }

  } catch (error) {
    logger.error('Ошибка при валидации токена:', error);
    res.status(500).json({ 
      valid: false,
      error: 'Ошибка при валидации токена',
      details: error.message 
    });
  }
});

/**
 * Получение информации о пользователе
 */
router.get('/yandex/user', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Токен доступа не предоставлен' });
    }

    const access_token = authHeader.split(' ')[1];

    const response = await axios.get(`${process.env.YANDEX_OAUTH_URL}/info`, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });

    res.json({
      user: response.data,
      message: 'Информация о пользователе получена'
    });

  } catch (error) {
    logger.error('Ошибка при получении информации о пользователе:', error);
    res.status(500).json({ 
      error: 'Не удалось получить информацию о пользователе',
      details: error.message 
    });
  }
});

module.exports = router;
