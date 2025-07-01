/**
 * Утилиты для тестирования
 */

// Генерация тестовых данных
const generateTestPageData = (overrides = {}) => {
  return {
    url: 'https://example.com/test-page',
    title: 'Тестовая страница',
    meta_description: 'Описание тестовой страницы для проверки функциональности',
    meta_keywords: ['тестирование', 'автоматизация', 'реклама'],
    content: 'Контент тестовой страницы с ключевыми словами для генерации объявлений',
    ...overrides
  };
};

const generateTestAds = (count = 2) => {
  return Array(count).fill().map((_, index) => ({
    Title: `Заголовок объявления ${index + 1}`,
    Text: `Текст объявления ${index + 1} с призывом к действию`,
    DisplayUrl: 'example.com',
    SiteLinks: []
  }));
};

const generateTestCampaign = (overrides = {}) => {
  return {
    Id: 12345,
    Name: 'Тестовая кампания',
    Status: 'SERVING',
    Type: 'TEXT_CAMPAIGN',
    DailyBudget: {
      Amount: 1000000000, // 1000 руб в копейках
      Mode: 'DISTRIBUTED'
    },
    ...overrides
  };
};

// Моки для внешних сервисов
const mockYandexDirectService = () => {
  return {
    getCampaigns: jest.fn().mockResolvedValue({
      Campaigns: [generateTestCampaign()]
    }),
    createCampaign: jest.fn().mockResolvedValue({
      AddResults: [{ Id: 12345, Warnings: [] }]
    }),
    getAds: jest.fn().mockResolvedValue({
      Ads: generateTestAds()
    }),
    createAds: jest.fn().mockResolvedValue({
      AddResults: [
        { Id: 67890, Warnings: [] },
        { Id: 67891, Warnings: [] }
      ]
    }),
    validateToken: jest.fn().mockResolvedValue(true)
  };
};

const mockOpenAIService = () => {
  return {
    generateAds: jest.fn().mockResolvedValue(generateTestAds())
  };
};

const mockFileProcessor = () => {
  return {
    parseFile: jest.fn().mockResolvedValue(generateTestPageData()),
    parseYamlFile: jest.fn().mockImplementation((content) => {
      return generateTestPageData({ title: 'Parsed from YAML' });
    }),
    parseMarkdownFile: jest.fn().mockImplementation((content) => {
      return generateTestPageData({ title: 'Parsed from Markdown' });
    }),
    parseTxtFile: jest.fn().mockImplementation((content) => {
      return generateTestPageData({ title: 'Parsed from TXT' });
    })
  };
};

// Утилиты для создания запросов
const createAuthenticatedRequest = (request, token = 'valid_test_token') => {
  return request.set('Authorization', `Bearer ${token}`);
};

const createFileUploadRequest = (request, fileName = 'test.yaml', content = 'url: https://example.com\ntitle: Test') => {
  return request.attach('file', Buffer.from(content), fileName);
};

// Валидаторы ответов
const validateSuccessResponse = (response) => {
  expect(response.body).toHaveProperty('success', true);
  expect(response.status).toBe(200);
};

const validateErrorResponse = (response, expectedStatus = 400) => {
  expect(response.body).toHaveProperty('error');
  expect(response.status).toBe(expectedStatus);
};

const validateCampaignResponse = (response) => {
  validateSuccessResponse(response);
  expect(response.body).toHaveProperty('campaignId');
  expect(typeof response.body.campaignId).toBe('number');
};

const validateAdsResponse = (response) => {
  validateSuccessResponse(response);
  expect(response.body).toHaveProperty('ads');
  expect(Array.isArray(response.body.ads)).toBe(true);
  if (response.body.ads.length > 0) {
    expect(response.body.ads[0]).toHaveProperty('Title');
    expect(response.body.ads[0]).toHaveProperty('Text');
  }
};

// Утилиты для проверки производительности
const measureResponseTime = async (requestPromise) => {
  const startTime = Date.now();
  const response = await requestPromise;
  const responseTime = Date.now() - startTime;
  return { response, responseTime };
};

const expectResponseTime = (responseTime, maxTime) => {
  expect(responseTime).toBeLessThan(maxTime);
};

// Утилиты для тестирования ошибок
const createNetworkError = (message = 'Network Error') => {
  const error = new Error(message);
  error.code = 'ECONNREFUSED';
  return error;
};

const createAPIError = (status = 500, message = 'API Error') => {
  const error = new Error(message);
  error.response = {
    status,
    data: { error: message }
  };
  return error;
};

const createTimeoutError = () => {
  const error = new Error('Timeout');
  error.code = 'ETIMEDOUT';
  return error;
};

// Утилиты для проверки безопасности
const createXSSPayload = (type = 'script') => {
  const payloads = {
    script: '<script>alert("xss")</script>',
    img: '<img src="x" onerror="alert(1)">',
    svg: '<svg onload="alert(1)">',
    iframe: '<iframe src="javascript:alert(1)"></iframe>'
  };
  return payloads[type] || payloads.script;
};

const createSQLInjectionPayload = () => {
  return "'; DROP TABLE campaigns; --";
};

const createPathTraversalPayload = () => {
  return '../../../etc/passwd';
};

// Очистка тестовых данных
const cleanupTestData = () => {
  // Здесь можно добавить логику очистки тестовых файлов, БД и т.д.
  // В текущей реализации используются моки, поэтому очистка не требуется
};

module.exports = {
  // Генераторы данных
  generateTestPageData,
  generateTestAds,
  generateTestCampaign,

  // Моки сервисов
  mockYandexDirectService,
  mockOpenAIService,
  mockFileProcessor,

  // Утилиты для запросов
  createAuthenticatedRequest,
  createFileUploadRequest,

  // Валидаторы
  validateSuccessResponse,
  validateErrorResponse,
  validateCampaignResponse,
  validateAdsResponse,

  // Производительность
  measureResponseTime,
  expectResponseTime,

  // Обработка ошибок
  createNetworkError,
  createAPIError,
  createTimeoutError,

  // Безопасность
  createXSSPayload,
  createSQLInjectionPayload,
  createPathTraversalPayload,

  // Очистка
  cleanupTestData
};
