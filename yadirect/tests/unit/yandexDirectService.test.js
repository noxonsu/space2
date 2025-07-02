const YandexDirectService = require('../../src/services/yandexDirectService');
const axios = require('axios');

// Мокаем axios
jest.mock('axios');
const mockedAxios = axios;

describe('YandexDirectService', () => {
  let yandexService;
  const mockToken = 'mock_access_token';

  beforeEach(() => {
    jest.clearAllMocks();
    yandexService = new YandexDirectService(mockToken);
  });

  describe('constructor', () => {
    test('should initialize with correct properties', () => {
      expect(yandexService.accessToken).toBe(mockToken);
      expect(yandexService.apiUrl).toBe('https://api.direct.yandex.com/json/v5');
      expect(yandexService.headers).toEqual({
        'Authorization': `Bearer ${mockToken}`,
        'Content-Type': 'application/json',
        'Accept-Language': 'ru'
      });
    });

    test('should use custom API URL from environment', () => {
      process.env.YANDEX_DIRECT_API_URL = 'https://custom.api.url';
      const service = new YandexDirectService(mockToken);
      expect(service.apiUrl).toBe('https://custom.api.url');
      delete process.env.YANDEX_DIRECT_API_URL;
    });
  });

  describe('validateToken', () => {
    test('should validate token successfully', async () => {
      const mockResponse = {
        data: {
          result: {
            Campaigns: []
          }
        }
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const result = await yandexService.validateToken();

      expect(result.valid).toBe(true);
      expect(result.campaigns).toEqual({ Campaigns: [] });
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'https://api.direct.yandex.com/json/v5/campaigns',
        {
          method: 'get',
          params: {
            SelectionCriteria: {},
            FieldNames: ['Id'],
            Page: {
              Limit: 1,
              Offset: 0
            }
          }
        },
        { headers: yandexService.headers }
      );
    });

    test('should throw error for 401 status', async () => {
      const mockError = {
        response: { status: 401 }
      };

      mockedAxios.post.mockRejectedValue(mockError);

      await expect(yandexService.validateToken()).rejects.toThrow('Недействительный токен авторизации');
    });

    test('should throw error for 403 status', async () => {
      const mockError = {
        response: { status: 403 }
      };

      mockedAxios.post.mockRejectedValue(mockError);

      await expect(yandexService.validateToken()).rejects.toThrow('Недостаточно прав доступа');
    });

    test('should throw generic error for other statuses', async () => {
      const mockError = {
        message: 'Network error'
      };

      mockedAxios.post.mockRejectedValue(mockError);

      await expect(yandexService.validateToken()).rejects.toThrow('Ошибка API: Network error');
    });
  });

  describe('getCampaigns', () => {
    test('should get campaigns successfully', async () => {
      const mockResponse = {
        data: {
          result: {
            Campaigns: [
              { Id: 1, Name: 'Campaign 1', Status: 'ACCEPTED' },
              { Id: 2, Name: 'Campaign 2', Status: 'DRAFT' }
            ]
          }
        }
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const result = await yandexService.getCampaigns();

      expect(result).toEqual(mockResponse.data.result);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'https://api.direct.yandex.com/json/v5/campaigns',
        {
          method: 'get',
          params: {
            SelectionCriteria: {},
            FieldNames: ['Id', 'Name', 'Status', 'State', 'Type']
          }
        },
        { headers: yandexService.headers }
      );
    });

    test('should handle API error with error_string', async () => {
      const mockError = {
        response: {
          status: 400,
          data: {
            error: {
              error_string: 'Invalid request format'
            }
          }
        }
      };

      mockedAxios.post.mockRejectedValue(mockError);

      await expect(yandexService.getCampaigns()).rejects.toThrow('Не удалось получить кампании: Invalid request format');
    });
  });

  describe('createCampaign', () => {
    const mockData = {
      url: 'https://example.com',
      title: 'Test Campaign',
      meta_keywords: ['keyword1', 'keyword2'],
      main_keyword: 'keyword1'
    };

    const mockGeneratedAds = [
      {
        title: 'Ad Title',
        description: 'Ad Description',
        url: 'https://example.com'
      }
    ];

    test('should create campaign successfully', async () => {
      // Mock campaign creation
      const campaignResponse = {
        data: {
          result: {
            AddResults: [{ Id: 12345 }]
          }
        }
      };

      // Mock ad group creation
      const adGroupResponse = {
        data: {
          result: {
            AddResults: [{ Id: 67890 }]
          }
        }
      };

      // Mock ads creation
      const adsResponse = {
        data: {
          result: {
            AddResults: [{ Id: 111 }, { Id: 222 }]
          }
        }
      };

      // Mock keywords creation
      const keywordsResponse = {
        data: {
          result: {
            AddResults: [{ Id: 333 }, { Id: 444 }]
          }
        }
      };

      mockedAxios.post
        .mockResolvedValueOnce(campaignResponse)
        .mockResolvedValueOnce(adGroupResponse)
        .mockResolvedValueOnce(adsResponse)
        .mockResolvedValueOnce(keywordsResponse);

      const result = await yandexService.createCampaign(mockData, mockGeneratedAds);

      expect(result).toEqual({
        campaignId: 12345,
        adGroupId: 67890,
        adsCreated: 2,
        keywordsCreated: 2
      });

      // Verify campaign creation call
      expect(mockedAxios.post).toHaveBeenNthCalledWith(1,
        'https://api.direct.yandex.com/json/v5/campaigns',
        {
          method: 'add',
          params: {
            Campaigns: [{
              Name: expect.stringContaining('keyword1'),
              Type: 'TEXT_CAMPAIGN',
              Status: 'DRAFT',
              TextCampaign: {
                BiddingStrategy: {
                  Search: {
                    BiddingStrategyType: 'HIGHEST_POSITION'
                  },
                  Network: {
                    BiddingStrategyType: 'SERVING_OFF'
                  }
                },
                Settings: [{
                  Option: 'ADD_METRICA_TAG',
                  Value: 'YES'
                }]
              }
            }]
          }
        },
        { headers: yandexService.headers }
      );
    });

    test('should throw error when campaign creation fails', async () => {
      const mockError = new Error('Campaign creation failed');
      mockedAxios.post.mockRejectedValue(mockError);

      await expect(yandexService.createCampaign(mockData, mockGeneratedAds))
        .rejects.toThrow('Не удалось создать кампанию: Campaign creation failed');
    });
  });

  describe('createAdGroup', () => {
    test('should create ad group successfully', async () => {
      const mockResponse = {
        data: {
          result: {
            AddResults: [{ Id: 67890 }]
          }
        }
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const mockData = {
        main_keyword: 'test keyword'
      };

      const result = await yandexService.createAdGroup(12345, mockData);

      expect(result).toEqual({ adGroupId: 67890 });
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'https://api.direct.yandex.com/json/v5/adgroups',
        {
          method: 'add',
          params: {
            AdGroups: [{
              Name: 'Группа: test keyword',
              CampaignId: 12345,
              RegionIds: [213],
              NegativeKeywords: [],
              TrackingParams: 'utm_source=yandex&utm_medium=cpc&utm_campaign=12345'
            }]
          }
        },
        { headers: yandexService.headers }
      );
    });
  });

  describe('createAds', () => {
    test('should create ads successfully', async () => {
      const mockResponse = {
        data: {
          result: {
            AddResults: [{ Id: 111 }, { Id: 222 }]
          }
        }
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const mockAds = [
        {
          title: 'Ad 1',
          title2: 'Subtitle 1',
          description: 'Description 1',
          url: 'https://example.com',
          displayPath: 'path1'
        },
        {
          title: 'Ad 2',
          description: 'Description 2',
          url: 'https://example.com'
        }
      ];

      const result = await yandexService.createAds(67890, mockAds);

      expect(result).toHaveLength(2);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'https://api.direct.yandex.com/json/v5/ads',
        {
          method: 'add',
          params: {
            Ads: [
              {
                AdGroupId: 67890,
                TextAd: {
                  Title: 'Ad 1',
                  Title2: 'Subtitle 1',
                  Text: 'Description 1',
                  Href: 'https://example.com',
                  Mobile: 'YES',
                  DisplayUrlPath: 'path1'
                }
              },
              {
                AdGroupId: 67890,
                TextAd: {
                  Title: 'Ad 2',
                  Title2: '',
                  Text: 'Description 2',
                  Href: 'https://example.com',
                  Mobile: 'YES',
                  DisplayUrlPath: ''
                }
              }
            ]
          }
        },
        { headers: yandexService.headers }
      );
    });
  });

  describe('createKeywords', () => {
    test('should create keywords successfully', async () => {
      const mockResponse = {
        data: {
          result: {
            AddResults: [{ Id: 333 }, { Id: 444 }]
          }
        }
      };

      mockedAxios.post.mockResolvedValue(mockResponse);

      const keywords = ['keyword1', 'keyword2'];

      const result = await yandexService.createKeywords(67890, keywords);

      expect(result).toHaveLength(2);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'https://api.direct.yandex.com/json/v5/keywords',
        {
          method: 'add',
          params: {
            Keywords: [
              {
                AdGroupId: 67890,
                Keyword: 'keyword1',
                UserParam1: '',
                UserParam2: '',
                Bid: 100000000
              },
              {
                AdGroupId: 67890,
                Keyword: 'keyword2',
                UserParam1: '',
                UserParam2: '',
                Bid: 100000000
              }
            ]
          }
        },
        { headers: yandexService.headers }
      );
    });
  });

  describe('generateCampaignName', () => {
    test('should generate campaign name with date', () => {
      const mockData = { main_keyword: 'test keyword' };
      const name = yandexService.generateCampaignName(mockData);
      
      expect(name).toContain('test keyword');
      expect(name).toMatch(/\d{4}-\d{2}-\d{2}/); // Should contain date
    });

    test('should use default name when main_keyword is missing', () => {
      const mockData = {};
      const name = yandexService.generateCampaignName(mockData);
      
      expect(name).toContain('Кампания');
    });
  });

  describe('generateAdGroupName', () => {
    test('should generate ad group name', () => {
      const mockData = { main_keyword: 'test keyword' };
      const name = yandexService.generateAdGroupName(mockData);
      
      expect(name).toBe('Группа: test keyword');
    });

    test('should use default name when main_keyword is missing', () => {
      const mockData = {};
      const name = yandexService.generateAdGroupName(mockData);
      
      expect(name).toBe('Группа: Основная');
    });
  });
});
