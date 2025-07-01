const request = require('supertest');
const express = require('express');
const campaignsRouter = require('../../src/routes/campaigns');
const YandexDirectService = require('../../src/services/yandexDirectService');
const OpenAIService = require('../../src/services/openaiService');

// Mock сервисов
jest.mock('../../src/services/yandexDirectService');
jest.mock('../../src/services/openaiService');
jest.mock('../../src/utils/logger', () => ({
  error: jest.fn(),
  info: jest.fn()
}));

describe('Campaigns Routes', () => {
  let app;
  let mockYandexService;
  let mockOpenAIService;

  beforeEach(() => {
    app = express();
    app.use(express.json());
    app.use('/campaigns', campaignsRouter);
    
    // Настройка моков
    mockYandexService = {
      getCampaigns: jest.fn(),
      createCampaign: jest.fn(),
      getAds: jest.fn(),
      createAds: jest.fn()
    };
    
    mockOpenAIService = {
      generateAds: jest.fn()
    };

    YandexDirectService.mockImplementation(() => mockYandexService);
    OpenAIService.mockImplementation(() => mockOpenAIService);

    jest.clearAllMocks();
  });

  describe('Authentication middleware', () => {
    test('should reject requests without Authorization header', async () => {
      const response = await request(app)
        .get('/campaigns')
        .expect(401);

      expect(response.body).toHaveProperty('error', 'Токен доступа не предоставлен');
    });

    test('should reject requests with invalid Authorization format', async () => {
      const response = await request(app)
        .get('/campaigns')
        .set('Authorization', 'InvalidFormat token')
        .expect(401);

      expect(response.body).toHaveProperty('error', 'Токен доступа не предоставлен');
    });

    test('should allow requests with valid Bearer token', async () => {
      mockYandexService.getCampaigns.mockResolvedValue({ Campaigns: [] });

      await request(app)
        .get('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(200);
    });
  });

  describe('GET /campaigns', () => {
    test('should return list of campaigns', async () => {
      const mockCampaigns = {
        Campaigns: [
          { Id: 1, Name: 'Кампания 1', Status: 'SERVING' },
          { Id: 2, Name: 'Кампания 2', Status: 'PAUSED' }
        ]
      };

      mockYandexService.getCampaigns.mockResolvedValue(mockCampaigns);

      const response = await request(app)
        .get('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        campaigns: mockCampaigns.Campaigns,
        total: 2
      });

      expect(mockYandexService.getCampaigns).toHaveBeenCalledTimes(1);
    });

    test('should handle empty campaigns list', async () => {
      mockYandexService.getCampaigns.mockResolvedValue({});

      const response = await request(app)
        .get('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        campaigns: [],
        total: 0
      });
    });

    test('should handle service errors', async () => {
      mockYandexService.getCampaigns.mockRejectedValue(new Error('API Error'));

      const response = await request(app)
        .get('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Не удалось получить список кампаний');
      expect(response.body).toHaveProperty('details', 'API Error');
    });
  });

  describe('POST /campaigns', () => {
    const validPageData = {
      url: 'https://example.com',
      title: 'Test Page',
      meta_description: 'Test description',
      meta_keywords: ['keyword1', 'keyword2']
    };

    test('should create campaign with generated ads', async () => {
      const mockGeneratedAds = [
        { Title: 'Заголовок 1', Text: 'Текст объявления 1' },
        { Title: 'Заголовок 2', Text: 'Текст объявления 2' }
      ];

      const mockCampaignResult = {
        AddResults: [{ Id: 12345 }]
      };

      const mockAdsResult = {
        AddResults: [{ Id: 67890 }]
      };

      mockOpenAIService.generateAds.mockResolvedValue(mockGeneratedAds);
      mockYandexService.createCampaign.mockResolvedValue(mockCampaignResult);
      mockYandexService.createAds.mockResolvedValue(mockAdsResult);

      const response = await request(app)
        .post('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({ pageData: validPageData, generateAds: true })
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('campaignId', 12345);
      expect(response.body).toHaveProperty('generatedAds', mockGeneratedAds);
      expect(response.body).toHaveProperty('adsResult', mockAdsResult);

      expect(mockOpenAIService.generateAds).toHaveBeenCalledWith(validPageData);
      expect(mockYandexService.createCampaign).toHaveBeenCalled();
      expect(mockYandexService.createAds).toHaveBeenCalled();
    });

    test('should create campaign without generating ads', async () => {
      const mockCampaignResult = {
        AddResults: [{ Id: 12345 }]
      };

      mockYandexService.createCampaign.mockResolvedValue(mockCampaignResult);

      const response = await request(app)
        .post('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({ pageData: validPageData, generateAds: false })
        .expect(200);

      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('campaignId', 12345);
      expect(response.body).not.toHaveProperty('generatedAds');

      expect(mockOpenAIService.generateAds).not.toHaveBeenCalled();
      expect(mockYandexService.createAds).not.toHaveBeenCalled();
    });

    test('should reject request without pageData', async () => {
      const response = await request(app)
        .post('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({ generateAds: true })
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Данные страницы не предоставлены');
    });

    test('should handle OpenAI service errors', async () => {
      mockOpenAIService.generateAds.mockRejectedValue(new Error('OpenAI API Error'));

      const response = await request(app)
        .post('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({ pageData: validPageData, generateAds: true })
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Ошибка при создании кампании');
      expect(response.body).toHaveProperty('details', 'OpenAI API Error');
    });

    test('should handle campaign creation errors', async () => {
      mockOpenAIService.generateAds.mockResolvedValue([]);
      mockYandexService.createCampaign.mockRejectedValue(new Error('Campaign creation failed'));

      const response = await request(app)
        .post('/campaigns')
        .set('Authorization', 'Bearer valid_token')
        .send({ pageData: validPageData, generateAds: true })
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Ошибка при создании кампании');
    });
  });

  describe('GET /campaigns/:campaignId/ads', () => {
    test('should return ads for campaign', async () => {
      const mockAds = {
        Ads: [
          { Id: 1, Headline: 'Заголовок 1' },
          { Id: 2, Headline: 'Заголовок 2' }
        ]
      };

      mockYandexService.getAds.mockResolvedValue(mockAds);

      const response = await request(app)
        .get('/campaigns/12345/ads')
        .set('Authorization', 'Bearer valid_token')
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        ads: mockAds.Ads,
        total: 2
      });

      expect(mockYandexService.getAds).toHaveBeenCalledWith('12345');
    });

    test('should handle invalid campaign ID', async () => {
      const response = await request(app)
        .get('/campaigns/invalid/ads')
        .set('Authorization', 'Bearer valid_token')
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Некорректный ID кампании');
    });

    test('should handle service errors when getting ads', async () => {
      mockYandexService.getAds.mockRejectedValue(new Error('Ads fetch error'));

      const response = await request(app)
        .get('/campaigns/12345/ads')
        .set('Authorization', 'Bearer valid_token')
        .expect(500);

      expect(response.body).toHaveProperty('error', 'Не удалось получить объявления');
    });
  });

  describe('POST /campaigns/:campaignId/ads', () => {
    const validAdsData = [
      { Title: 'Заголовок 1', Text: 'Текст 1' },
      { Title: 'Заголовок 2', Text: 'Текст 2' }
    ];

    test('should create ads for campaign', async () => {
      const mockResult = {
        AddResults: [{ Id: 67890 }, { Id: 67891 }]
      };

      mockYandexService.createAds.mockResolvedValue(mockResult);

      const response = await request(app)
        .post('/campaigns/12345/ads')
        .set('Authorization', 'Bearer valid_token')
        .send({ ads: validAdsData })
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        result: mockResult
      });

      expect(mockYandexService.createAds).toHaveBeenCalledWith('12345', validAdsData);
    });

    test('should reject request without ads data', async () => {
      const response = await request(app)
        .post('/campaigns/12345/ads')
        .set('Authorization', 'Bearer valid_token')
        .send({})
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Данные объявлений не предоставлены');
    });

    test('should reject empty ads array', async () => {
      const response = await request(app)
        .post('/campaigns/12345/ads')
        .set('Authorization', 'Bearer valid_token')
        .send({ ads: [] })
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Данные объявлений не предоставлены');
    });

    test('should handle invalid campaign ID when creating ads', async () => {
      const response = await request(app)
        .post('/campaigns/invalid/ads')
        .set('Authorization', 'Bearer valid_token')
        .send({ ads: validAdsData })
        .expect(400);

      expect(response.body).toHaveProperty('error', 'Некорректный ID кампании');
    });
  });
});
