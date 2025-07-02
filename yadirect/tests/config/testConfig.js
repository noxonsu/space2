/**
 * Конфигурация для тестов
 */

module.exports = {
  // API endpoints
  endpoints: {
    status: '/api/status',
    auth: {
      yandexUrl: '/api/auth/yandex/url',
      yandexCallback: '/api/auth/yandex/callback',
      refresh: '/api/auth/refresh'
    },
    campaigns: {
      list: '/api/campaigns',
      create: '/api/campaigns',
      ads: (campaignId) => `/api/campaigns/${campaignId}/ads`
    },
    upload: '/api/upload',
    generateAds: '/api/generate-ads'
  },

  // Временные ограничения для разных типов тестов
  timeouts: {
    unit: 5000,
    integration: 10000,
    e2e: 30000,
    performance: 60000,
    security: 15000
  },

  // Лимиты производительности
  performance: {
    maxResponseTime: {
      healthcheck: 100,
      campaigns: 2000,
      adGeneration: 5000,
      fileUpload: 3000
    },
    concurrentRequests: {
      light: 10,
      medium: 20,
      heavy: 50
    },
    maxPayloadSize: 10 * 1024 * 1024 // 10MB
  },

  // Тестовые токены и ключи
  testTokens: {
    valid: 'valid_test_token_12345',
    expired: 'expired_test_token_67890',
    invalid: 'invalid_test_token_abcdef',
    malformed: 'malformed..token..xyz'
  },

  // Тестовые данные по умолчанию
  defaultData: {
    pageData: {
      url: 'https://example.com/test',
      title: 'Тестовая страница',
      meta_description: 'Описание для тестирования',
      meta_keywords: ['тест', 'автоматизация', 'реклама'],
      content: 'Тестовый контент страницы'
    },
    campaign: {
      name: 'Тестовая кампания',
      dailyBudget: 1000,
      strategy: 'AVERAGE_CPC'
    },
    ads: {
      count: 3,
      maxTitleLength: 56,
      maxTextLength: 90
    }
  },

  // Конфигурация для безопасности
  security: {
    maliciousPayloads: {
      xss: [
        '<script>alert("xss")</script>',
        'javascript:alert("xss")',
        '<img src="x" onerror="alert(1)">',
        '"><script>alert(document.cookie)</script>'
      ],
      sqlInjection: [
        "'; DROP TABLE campaigns; --",
        "' OR '1'='1",
        "'; SELECT * FROM users; --",
        "1' UNION SELECT * FROM passwords--"
      ],
      pathTraversal: [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\config\\sam',
        '/etc/shadow',
        'C:\\Windows\\System32\\drivers\\etc\\hosts'
      ]
    },
    forbiddenFileTypes: [
      '.exe', '.bat', '.sh', '.php', '.asp', '.jsp',
      '.cmd', '.com', '.scr', '.vbs', '.js'
    ],
    maxFileSize: 5 * 1024 * 1024 // 5MB
  },

  // Настройки для нагрузочного тестирования
  load: {
    rapidRequests: 100,
    burstRequests: 20,
    stressIterations: 100,
    concurrentUsers: 50
  },

  // Пороги покрытия кода
  coverage: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    },
    perFile: {
      branches: 60,
      functions: 60,
      lines: 60,
      statements: 60
    }
  },

  // Настройки среды
  environment: {
    test: {
      NODE_ENV: 'test',
      LOG_LEVEL: 'silent',
      PORT: 3001
    },
    development: {
      NODE_ENV: 'development', 
      LOG_LEVEL: 'debug',
      PORT: 3000
    }
  },

  // Mock данные для внешних API
  mocks: {
    yandexDirect: {
      baseUrl: 'https://api.direct.yandex.com/json/v5',
      campaigns: {
        success: {
          Campaigns: [
            {
              Id: 12345,
              Name: 'Тестовая кампания 1',
              Status: 'SERVING',
              Type: 'TEXT_CAMPAIGN'
            },
            {
              Id: 12346,
              Name: 'Тестовая кампания 2',
              Status: 'PAUSED',
              Type: 'TEXT_CAMPAIGN'
            }
          ]
        },
        empty: { Campaigns: [] }
      },
      ads: {
        success: {
          Ads: [
            {
              Id: 67890,
              CampaignId: 12345,
              AdGroupId: 54321,
              Status: 'ACCEPTED',
              Type: 'TEXT_AD',
              Title: 'Заголовок объявления',
              Text: 'Текст объявления'
            }
          ]
        }
      }
    },
    openai: {
      apiKey: 'test_openai_key',
      responses: {
        ads: [
          {
            Title: 'Сгенерированный заголовок 1',
            Text: 'Сгенерированный текст объявления 1',
            DisplayUrl: 'example.com'
          },
          {
            Title: 'Сгенерированный заголовок 2', 
            Text: 'Сгенерированный текст объявления 2',
            DisplayUrl: 'example.com'
          }
        ]
      }
    }
  }
};
