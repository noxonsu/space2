const OpenAI = require('openai');
const logger = require('../utils/logger');

class OpenAIService {
  constructor() {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    });
  }

  /**
   * Генерация объявлений на основе данных страницы
   */
  async generateAds(pageData) {
    try {
      const prompt = this.buildPrompt(pageData);
      
      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: `Ты - эксперт по созданию рекламных объявлений для Яндекс.Директ. 
            Создавай эффективные объявления, которые соответствуют требованиям Яндекса:
            - Заголовок: до 35 символов
            - Второй заголовок: до 30 символов (опционально)
            - Описание: до 75 символов
            - Объявления должны быть релевантными и привлекательными
            - Используй ключевые слова из предоставленных данных`
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 1500
      });

      const generatedContent = response.choices[0].message.content;
      return this.parseGeneratedAds(generatedContent, pageData.url);

    } catch (error) {
      logger.error('Ошибка при генерации объявлений:', error);
      throw new Error(`Не удалось сгенерировать объявления: ${error.message}`);
    }
  }

  /**
   * Построение промпта для генерации объявлений
   */
  buildPrompt(pageData) {
    return `
Создай 3-5 рекламных объявлений для Яндекс.Директ на основе следующих данных:

URL: ${pageData.url}
Заголовок страницы: ${pageData.title}
Описание: ${pageData.meta_description}
Основное ключевое слово: ${pageData.main_keyword}

Ключевые слова:
${pageData.meta_keywords.map(keyword => `- ${keyword}`).join('\n')}

Связанные ключевые слова:
${pageData.related_keywords.map(keyword => `- ${keyword}`).join('\n')}

Верни результат в следующем JSON формате:
{
  "ads": [
    {
      "title": "Заголовок объявления (до 35 символов)",
      "title2": "Второй заголовок (до 30 символов, опционально)",
      "description": "Описание объявления (до 75 символов)",
      "displayPath": "путь/отображения"
    }
  ]
}

Убедись, что:
1. Объявления релевантны теме страницы
2. Используются ключевые слова из списка
3. Соблюдены ограничения по длине
4. Объявления привлекательны для целевой аудитории
5. Есть призыв к действию
`;
  }

  /**
   * Парсинг сгенерированных объявлений
   */
  parseGeneratedAds(content, url) {
    try {
      // Пытаемся найти JSON в ответе
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return parsed.ads.map(ad => ({
          ...ad,
          url: url
        }));
      }

      // Если JSON не найден, пытаемся распарсить текстовый формат
      return this.parseTextFormat(content, url);

    } catch (error) {
      logger.error('Ошибка при парсинге объявлений:', error);
      
      // Возвращаем базовое объявление как fallback
      return [{
        title: 'Профессиональные услуги',
        title2: 'Онлайн консультация',
        description: 'Получите профессиональную помощь. Быстро и надежно!',
        url: url,
        displayPath: 'services'
      }];
    }
  }

  /**
   * Парсинг текстового формата
   */
  parseTextFormat(content, url) {
    const ads = [];
    const lines = content.split('\n').filter(line => line.trim());
    
    let currentAd = {};
    
    for (const line of lines) {
      const trimmed = line.trim();
      
      if (trimmed.startsWith('Заголовок:') || trimmed.startsWith('Title:')) {
        if (Object.keys(currentAd).length > 0) {
          ads.push({ ...currentAd, url });
          currentAd = {};
        }
        currentAd.title = trimmed.split(':')[1]?.trim() || '';
      } else if (trimmed.startsWith('Второй заголовок:') || trimmed.startsWith('Title2:')) {
        currentAd.title2 = trimmed.split(':')[1]?.trim() || '';
      } else if (trimmed.startsWith('Описание:') || trimmed.startsWith('Description:')) {
        currentAd.description = trimmed.split(':')[1]?.trim() || '';
      }
    }
    
    if (Object.keys(currentAd).length > 0) {
      ads.push({ ...currentAd, url });
    }

    return ads.length > 0 ? ads : [{
      title: 'Качественные услуги',
      title2: 'Быстро и надежно',
      description: 'Профессиональный подход. Гарантия результата.',
      url: url,
      displayPath: 'services'
    }];
  }

  /**
   * Генерация ключевых слов на основе контента
   */
  async generateKeywords(pageData) {
    try {
      const prompt = `
Проанализируй следующую информацию и сгенерируй дополнительные ключевые слова для рекламной кампании:

Заголовок: ${pageData.title}
Описание: ${pageData.meta_description}
Основное ключевое слово: ${pageData.main_keyword}

Существующие ключевые слова:
${pageData.meta_keywords.join(', ')}

Связанные ключевые слова:
${pageData.related_keywords.join(', ')}

Создай список из 10-15 дополнительных релевантных ключевых слов, которые могут использоваться в рекламной кампании.
Верни результат в виде простого списка, по одному ключевому слову на строке.
`;

      const response = await this.openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: 'Ты - эксперт по SEO и контекстной рекламе. Генерируй только релевантные ключевые слова.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.5,
        max_tokens: 500
      });

      const keywords = response.choices[0].message.content
        .split('\n')
        .map(line => line.replace(/^[-•\d\.]\s*/, '').trim())
        .filter(keyword => keyword.length > 0 && keyword.length < 100);

      return keywords;

    } catch (error) {
      logger.error('Ошибка при генерации ключевых слов:', error);
      return [];
    }
  }

  /**
   * Оптимизация объявления
   */
  async optimizeAd(adData, performance) {
    try {
      const prompt = `
Оптимизируй рекламное объявление на основе данных производительности:

Текущее объявление:
- Заголовок: ${adData.title}
- Описание: ${adData.description}

Статистика:
- Показы: ${performance.impressions}
- Клики: ${performance.clicks}
- CTR: ${performance.ctr}%
- Стоимость клика: ${performance.cpc} руб.

Предложи улучшенную версию объявления с объяснением изменений.
`;

      const response = await this.openai.chat.completions.create({
        model: 'gpt-4',
        messages: [
          {
            role: 'system',
            content: 'Ты - эксперт по оптимизации рекламных объявлений. Анализируй данные и предлагай конкретные улучшения.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.6,
        max_tokens: 800
      });

      return response.choices[0].message.content;

    } catch (error) {
      logger.error('Ошибка при оптимизации объявления:', error);
      throw error;
    }
  }
}

module.exports = OpenAIService;
