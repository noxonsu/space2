const axios = require('axios');
const logger = require('../utils/logger');

class YandexDirectService {
  constructor(accessToken) {
    this.accessToken = accessToken;
    this.apiUrl = process.env.YANDEX_DIRECT_API_URL || 'https://api.direct.yandex.com/json/v5';
    this.headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      'Accept-Language': 'ru'
    };
  }

  /**
   * Проверка корректности токена и доступности API
   */
  async validateToken() {
    try {
      const response = await axios.post(`${this.apiUrl}/campaigns`, {
        method: 'get',
        params: {
          SelectionCriteria: {},
          FieldNames: ['Id'],
          Page: {
            Limit: 1,
            Offset: 0
          }
        }
      }, { headers: this.headers });

      logger.info('Токен валиден, API доступен');
      return { valid: true, campaigns: response.data.result };
    } catch (error) {
      logger.error('Ошибка валидации токена:', error.response?.data || error.message);
      if (error.response?.status === 401) {
        throw new Error('Недействительный токен авторизации');
      } else if (error.response?.status === 403) {
        throw new Error('Недостаточно прав доступа');
      } else {
        throw new Error(`Ошибка API: ${error.message}`);
      }
    }
  }

  /**
   * Получение списка кампаний
   */
  async getCampaigns() {
    try {
      const response = await axios.post(`${this.apiUrl}/campaigns`, {
        method: 'get',
        params: {
          SelectionCriteria: {},
          FieldNames: ['Id', 'Name', 'Status', 'State', 'Type']
        }
      }, { headers: this.headers });

      return response.data.result;
    } catch (error) {
      logger.error('Ошибка при получении кампаний:', {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data
      });
      throw new Error(`Не удалось получить кампании: ${error.response?.data?.error?.error_string || error.message}`);
    }
  }

  /**
   * Создание новой кампании
   */
  async createCampaign(data, generatedAds) {
    try {
      const campaignData = {
        method: 'add',
        params: {
          Campaigns: [{
            Name: this.generateCampaignName(data),
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
      };

      const response = await axios.post(`${this.apiUrl}/campaigns`, campaignData, { 
        headers: this.headers 
      });

      if (response.data.result && response.data.result.AddResults) {
        const campaignId = response.data.result.AddResults[0].Id;
        logger.info(`Кампания создана с ID: ${campaignId}`);

        // Создаем группу объявлений
        const adGroupResult = await this.createAdGroup(campaignId, data);
        
        // Создаем объявления
        const adsResult = await this.createAds(adGroupResult.adGroupId, generatedAds);

        // Создаем ключевые слова
        const keywordsResult = await this.createKeywords(adGroupResult.adGroupId, data.meta_keywords);

        return {
          campaignId,
          adGroupId: adGroupResult.adGroupId,
          adsCreated: adsResult.length,
          keywordsCreated: keywordsResult.length
        };
      }

      throw new Error('Не удалось создать кампанию');
    } catch (error) {
      logger.error('Ошибка при создании кампании:', error);
      throw new Error(`Не удалось создать кампанию: ${error.message}`);
    }
  }

  /**
   * Создание группы объявлений
   */
  async createAdGroup(campaignId, data) {
    try {
      const adGroupData = {
        method: 'add',
        params: {
          AdGroups: [{
            Name: this.generateAdGroupName(data),
            CampaignId: campaignId,
            RegionIds: [213], // Москва по умолчанию
            NegativeKeywords: [],
            TrackingParams: `utm_source=yandex&utm_medium=cpc&utm_campaign=${campaignId}`
          }]
        }
      };

      const response = await axios.post(`${this.apiUrl}/adgroups`, adGroupData, { 
        headers: this.headers 
      });

      if (response.data.result && response.data.result.AddResults) {
        const adGroupId = response.data.result.AddResults[0].Id;
        logger.info(`Группа объявлений создана с ID: ${adGroupId}`);
        return { adGroupId };
      }

      throw new Error('Не удалось создать группу объявлений');
    } catch (error) {
      logger.error('Ошибка при создании группы объявлений:', error);
      throw error;
    }
  }

  /**
   * Создание объявлений
   */
  async createAds(adGroupId, generatedAds) {
    try {
      const adsData = generatedAds.map(ad => ({
        AdGroupId: adGroupId,
        TextAd: {
          Title: ad.title,
          Title2: ad.title2 || '',
          Text: ad.description,
          Href: ad.url,
          Mobile: 'YES',
          DisplayUrlPath: ad.displayPath || ''
        }
      }));

      const requestData = {
        method: 'add',
        params: {
          Ads: adsData
        }
      };

      const response = await axios.post(`${this.apiUrl}/ads`, requestData, { 
        headers: this.headers 
      });

      if (response.data.result && response.data.result.AddResults) {
        logger.info(`Создано объявлений: ${response.data.result.AddResults.length}`);
        return response.data.result.AddResults;
      }

      return [];
    } catch (error) {
      logger.error('Ошибка при создании объявлений:', error);
      throw error;
    }
  }

  /**
   * Создание ключевых слов
   */
  async createKeywords(adGroupId, keywords) {
    try {
      const keywordsData = keywords.map(keyword => ({
        AdGroupId: adGroupId,
        Keyword: keyword,
        UserParam1: '',
        UserParam2: '',
        Bid: 100000000 // 1 рубль в копейках
      }));

      const requestData = {
        method: 'add',
        params: {
          Keywords: keywordsData
        }
      };

      const response = await axios.post(`${this.apiUrl}/keywords`, requestData, { 
        headers: this.headers 
      });

      if (response.data.result && response.data.result.AddResults) {
        logger.info(`Создано ключевых слов: ${response.data.result.AddResults.length}`);
        return response.data.result.AddResults;
      }

      return [];
    } catch (error) {
      logger.error('Ошибка при создании ключевых слов:', error);
      throw error;
    }
  }

  /**
   * Генерация имени кампании
   */
  generateCampaignName(data) {
    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    return `${data.main_keyword || 'Кампания'} - ${dateStr}`;
  }

  /**
   * Генерация имени группы объявлений
   */
  generateAdGroupName(data) {
    return `Группа: ${data.main_keyword || 'Основная'}`;
  }

  /**
   * Получение статистики кампании
   */
  async getCampaignStats(campaignId) {
    try {
      const response = await axios.post(`${this.apiUrl}/reports`, {
        method: 'get',
        params: {
          SelectionCriteria: {
            CampaignIds: [campaignId]
          },
          FieldNames: ['Impressions', 'Clicks', 'Cost', 'Ctr'],
          ReportName: 'Campaign Statistics',
          ReportType: 'CAMPAIGN_PERFORMANCE_REPORT',
          DateRangeType: 'LAST_30_DAYS',
          Format: 'JSON'
        }
      }, { headers: this.headers });

      return response.data;
    } catch (error) {
      logger.error('Ошибка при получении статистики:', error);
      throw error;
    }
  }
}

module.exports = YandexDirectService;
