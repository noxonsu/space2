const express = require('express');
const YandexDirectService = require('../services/yandexDirectService');
const OpenAIService = require('../services/openaiService');
const logger = require('../utils/logger');

const router = express.Router();

// Middleware для проверки токена
const requireAuth = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Токен доступа не предоставлен' });
  }
  
  req.accessToken = authHeader.split(' ')[1];
  next();
};

/**
 * Получение списка кампаний
 */
router.get('/', requireAuth, async (req, res) => {
  try {
    const yandexService = new YandexDirectService(req.accessToken);
    const campaigns = await yandexService.getCampaigns();

    res.json({
      success: true,
      campaigns: campaigns.Campaigns || [],
      total: campaigns.Campaigns?.length || 0
    });

  } catch (error) {
    logger.error('Ошибка при получении кампаний:', error);
    res.status(500).json({ 
      error: 'Не удалось получить список кампаний',
      details: error.message 
    });
  }
});

/**
 * Создание новой кампании
 */
router.post('/', requireAuth, async (req, res) => {
  try {
    const { pageData, generateAds = true } = req.body;

    if (!pageData) {
      return res.status(400).json({ error: 'Данные страницы не предоставлены' });
    }

    const yandexService = new YandexDirectService(req.accessToken);
    let generatedAds = [];

    if (generateAds) {
      const openaiService = new OpenAIService();
      generatedAds = await openaiService.generateAds(pageData);
    }

    const result = await yandexService.createCampaign(pageData, generatedAds);

    const response = {
      success: true,
      campaignId: result.AddResults?.[0]?.Id || result.Id,
      message: 'Кампания успешно создана'
    };

    // Добавляем сгенерированные объявления и их результат только если они есть
    if (generatedAds && generatedAds.length > 0) {
      response.generatedAds = generatedAds;
      response.adsResult = result;
    }

    res.json(response);

  } catch (error) {
    logger.error('Ошибка при создании кампании:', error);
    res.status(500).json({ 
      error: 'Ошибка при создании кампании',
      details: error.message 
    });
  }
});

/**
 * Получение статистики кампании
 */
router.get('/:campaignId/stats', requireAuth, async (req, res) => {
  try {
    const { campaignId } = req.params;
    const yandexService = new YandexDirectService(req.accessToken);
    
    const stats = await yandexService.getCampaignStats(campaignId);

    res.json({
      success: true,
      campaignId,
      stats
    });

  } catch (error) {
    logger.error('Ошибка при получении статистики:', error);
    res.status(500).json({ 
      error: 'Не удалось получить статистику кампании',
      details: error.message 
    });
  }
});

/**
 * Генерация объявлений для существующих данных
 */
router.post('/generate-ads', requireAuth, async (req, res) => {
  try {
    const { pageData, count = 3 } = req.body;

    if (!pageData) {
      return res.status(400).json({ error: 'Данные страницы не предоставлены' });
    }

    const openaiService = new OpenAIService();
    const generatedAds = await openaiService.generateAds(pageData);

    // Ограничиваем количество объявлений
    const limitedAds = generatedAds.slice(0, count);

    res.json({
      success: true,
      ads: limitedAds,
      total: limitedAds.length,
      message: 'Объявления успешно сгенерированы'
    });

  } catch (error) {
    logger.error('Ошибка при генерации объявлений:', error);
    res.status(500).json({ 
      error: 'Не удалось сгенерировать объявления',
      details: error.message 
    });
  }
});

/**
 * Генерация ключевых слов
 */
router.post('/generate-keywords', requireAuth, async (req, res) => {
  try {
    const { pageData } = req.body;

    if (!pageData) {
      return res.status(400).json({ error: 'Данные страницы не предоставлены' });
    }

    const openaiService = new OpenAIService();
    const keywords = await openaiService.generateKeywords(pageData);

    res.json({
      success: true,
      keywords,
      total: keywords.length,
      message: 'Ключевые слова успешно сгенерированы'
    });

  } catch (error) {
    logger.error('Ошибка при генерации ключевых слов:', error);
    res.status(500).json({ 
      error: 'Не удалось сгенерировать ключевые слова',
      details: error.message 
    });
  }
});

/**
 * Оптимизация объявления на основе статистики
 */
router.post('/optimize-ad', requireAuth, async (req, res) => {
  try {
    const { adData, performance } = req.body;

    if (!adData || !performance) {
      return res.status(400).json({ 
        error: 'Данные объявления и статистика производительности обязательны' 
      });
    }

    const openaiService = new OpenAIService();
    const optimizedSuggestion = await openaiService.optimizeAd(adData, performance);

    res.json({
      success: true,
      originalAd: adData,
      performance,
      optimizationSuggestion: optimizedSuggestion,
      message: 'Рекомендации по оптимизации получены'
    });

  } catch (error) {
    logger.error('Ошибка при оптимизации объявления:', error);
    res.status(500).json({ 
      error: 'Не удалось оптимизировать объявление',
      details: error.message 
    });
  }
});

/**
 * Пример данных для тестирования
 */
router.get('/example', (req, res) => {
  const example = {
    pageData: {
      url: 'https://habab.ru/brachnogo-dogovora',
      title: 'Проверка договора брачного договора онлайн нейросетью',
      meta_description: 'Бесплатная онлайн проверка брачного договора с нейросетью: анализ условий, юридическая экспертиза и оценка условий брачного контракта',
      meta_keywords: [
        'проверка брачного договора',
        'анализ условий брачного договора',
        'юридическая проверка брачного договора',
        'экспертиза брачного договора',
        'оценка условий брачного контракта'
      ],
      related_keywords: [
        'юридическая экспертиза брачного договора',
        'консультация по брачному договору',
        'подбор условий брачного договора',
        'проверка договорных обязательств',
        'юридическая проверка соглашения'
      ],
      main_keyword: 'брачного договора'
    }
  };

  res.json({
    example,
    endpoints: {
      'POST /api/campaigns': 'Создание новой кампании',
      'GET /api/campaigns': 'Получение списка кампаний',
      'POST /api/campaigns/generate-ads': 'Генерация объявлений',
      'POST /api/campaigns/generate-keywords': 'Генерация ключевых слов',
      'GET /api/campaigns/:id/stats': 'Статистика кампании',
      'POST /api/campaigns/optimize-ad': 'Оптимизация объявления'
    }
  });
});

/**
 * GET /campaigns/:campaignId/ads
 * Получение объявлений кампании
 */
router.get('/:campaignId/ads', requireAuth, async (req, res) => {
  try {
    const { campaignId } = req.params;
    
    // Валидация ID кампании
    if (!/^\d+$/.test(campaignId)) {
      return res.status(400).json({ error: 'Некорректный ID кампании' });
    }

    const yandexService = new YandexDirectService(req.accessToken);
    const adsData = await yandexService.getAds(campaignId);

    res.json({
      success: true,
      ads: adsData.Ads || adsData,
      total: adsData.Ads ? adsData.Ads.length : adsData.length
    });

  } catch (error) {
    logger.error('Ошибка при получении объявлений:', error);
    res.status(500).json({ 
      error: 'Не удалось получить объявления',
      details: error.message 
    });
  }
});

/**
 * POST /campaigns/:campaignId/ads
 * Создание объявлений для кампании
 */
router.post('/:campaignId/ads', async (req, res) => {
  try {
    const { campaignId } = req.params;
    const { ads } = req.body;
    
    // Валидация ID кампании
    if (!/^\d+$/.test(campaignId)) {
      return res.status(400).json({ error: 'Некорректный ID кампании' });
    }

    // Валидация данных объявлений
    if (!ads || !Array.isArray(ads) || ads.length === 0) {
      return res.status(400).json({ error: 'Данные объявлений не предоставлены' });
    }

    const yandexDirect = new YandexDirectService(process.env.YANDEX_DIRECT_TOKEN);
    
    // Тут будет реальная логика создания объявлений
    // Пока возвращаем моковые данные
    const createdAds = ads.map((ad, index) => ({
      id: index + 1,
      ...ad,
      status: 'created'
    }));

    res.json({
      success: true,
      campaignId: parseInt(campaignId),
      ads: createdAds,
      message: 'Объявления успешно созданы'
    });

  } catch (error) {
    logger.error('Не удалось создать объявления:', error);
    res.status(500).json({ 
      error: 'Не удалось создать объявления',
      details: error.message 
    });
  }
});

module.exports = router;
