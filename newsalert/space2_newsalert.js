require('dotenv').config({ path: __dirname + '/.env' });
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');

const KEYWORDS_FILE_PATH = path.join(__dirname, '.env_keys');
const NEWS_DATA_FILE_PATH = path.join(__dirname, 'fetched_news.json');
const PROMPT_FILE_PATH = path.join(__dirname, '.env_prompt');
const BLACKLIST_FILE_PATH = path.join(__dirname, 'processed_urls_blacklist.json');
const SERPAPI_API_KEY = process.env.SERPAPI_KEY;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const SCRAPINGDOG_API_KEY = process.env.SCRAPINGDOG_API_KEY;
const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000; // 24 hours

// --- Admin Panel Code ---
const adminPort = 3656;

function parseBody(req, callback) {
  let body = '';
  req.on('data', chunk => {
    body += chunk.toString();
  });
  req.on('end', () => {
    try {
      const parsed = JSON.parse(body);
      callback(null, parsed);
    } catch (err) {
      callback(err, null);
    }
  });
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (pathname === '/' && method === 'GET') {
    const indexPath = path.join(__dirname, 'public', 'index.html');
    fs.readFile(indexPath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
  } else if (pathname === '/api/keywords' && method === 'GET') {
    fs.readFile(KEYWORDS_FILE_PATH, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading keywords file:', err);
        res.writeHead(500);
        res.end('Error reading keywords');
        return;
      }
      const keywords = data.split(/\r?\n/).map(line => line.trim()).filter(Boolean);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(keywords));
    });
  } else if (pathname === '/api/news' && method === 'GET') {
    fs.readFile(NEWS_DATA_FILE_PATH, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading news file:', err);
        res.writeHead(500);
        res.end('Error reading news');
        return;
      }
      let newsData = [];
      if (data) {
        try {
          newsData = JSON.parse(data);
        } catch (parseErr) {
          console.error('Error parsing news data:', parseErr);
          res.writeHead(500);
          res.end('Error parsing news data');
          return;
        }
      }
      
      const keyword = parsedUrl.query.keyword;
      if (keyword) {
        newsData = newsData.filter(item => item.keyword === keyword);
      }
      
      // Sort by fetchedAt descending (newest first)
      newsData.sort((a, b) => new Date(b.fetchedAt) - new Date(a.fetchedAt));
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(newsData));
    });
  } else if (pathname === '/api/keywords' && method === 'POST') {
    parseBody(req, (err, body) => {
      if (err || !body || !body.keyword) {
        res.writeHead(400);
        res.end('Keyword is required');
        return;
      }
      fs.appendFile(KEYWORDS_FILE_PATH, `\n${body.keyword}`, (err) => {
        if (err) {
          console.error('Error adding keyword:', err);
          res.writeHead(500);
          res.end('Error adding keyword');
          return;
        }
        res.writeHead(201);
        res.end('Keyword added');
      });
    });
  } else if (pathname.startsWith('/api/keywords/') && method === 'DELETE') {
    const keywordToDelete = decodeURIComponent(pathname.split('/').pop());
    fs.readFile(KEYWORDS_FILE_PATH, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading keywords file:', err);
        res.writeHead(500);
        res.end('Error reading keywords');
        return;
      }
      const keywords = data.split(/\r?\n/).map(line => line.trim()).filter(Boolean);
      const newKeywords = keywords.filter(k => k !== keywordToDelete);
      const newData = newKeywords.join('\n');
      fs.writeFile(KEYWORDS_FILE_PATH, newData, 'utf8', (err) => {
        if (err) {
          console.error('Error deleting keyword:', err);
          res.writeHead(500);
          res.end('Error deleting keyword');
          return;
        }
        res.writeHead(200);
        res.end('Keyword deleted');
      });
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// Запускаем сервер только если не в тестовой среде
if (process.env.NODE_ENV !== 'test') {
  server.listen(adminPort, () => {
    console.log(`Админ панель запущена на порту ${adminPort}`);
    console.log(`Admin panel listening at http://localhost:${adminPort}`);
  });
}
// --- End Admin Panel Code ---


async function sendTelegramMessage(chatId, text) {
    const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
    try {
        await axios.post(url, {
            chat_id: chatId,
            text: text,
            disable_web_page_preview: true // Optional: disable link previews
        });
        console.log('Telegram message sent successfully.');
    } catch (error) {
        console.error('Error sending Telegram message:', error.message);
        if (error.response && error.response.data) {
            console.error('Telegram API Error details:', error.response.data);
        }
    }
}

async function processNewsWithOpenAI(newsItem) {
    if (!OPENAI_API_KEY) {
        console.error('OpenAI API key not set. Skipping AI processing.');
        return null;
    }

    // Читаем промпт из файла
    let promptTemplate;
    try {
        promptTemplate = fs.readFileSync(PROMPT_FILE_PATH, 'utf8');
    } catch (error) {
        console.error('Error reading prompt file:', error.message);
        console.error('Using fallback prompt.');
        promptTemplate = `## УЛЬТИМАТИВНЫЕ ПРАВИЛА (9.98+/10)
1. Если новость не Sb₂O₃/сурьма → вернуть null.
2. Paywall/404 → summary_ru: "Статья недоступна", остальные поля null.
3. Обязательно сверяй CAS 1309‑64‑4 и HS 281820.
4. Числа — арабские, проценты со знаком %, объёмы в т, валюты — USD.
5. Глаголы ультрачёткие: «вырастет», «упадёт», «изменится», «снизится», «повысится».
6. Точные даты: «до 26 июн 2025».
7. Никаких эмоций — только ультрафакты, стратегии, деньги, риски.

Проанализируй эту новость:
{{NEWS_DATA}}

Верни только JSON-ответ в указанном формате или null если новость не про сурьму/Sb₂O₃.`;
    }

    // Заменяем плейсхолдер на данные новости
    const prompt = promptTemplate.replace('{{NEWS_DATA}}', JSON.stringify(newsItem, null, 2));

    try {
        console.log(`Processing news with OpenAI: "${newsItem.title}"`);
        
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-4o',
            messages: [
                {
                    role: 'system',
                    content: 'Ты — NAMAGIRI‑ASIM‑аналитик ChemPartners. Анализируешь только новости про Sb₂O₃ (триоксид сурьмы). Возвращаешь JSON в точном формате или null.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            temperature: 0.1,
            max_tokens: 2000
        }, {
            headers: {
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        let aiResponse = response.data.choices[0].message.content.trim();
        
        // Извлекаем JSON из Markdown блока, если он есть
        const jsonMatch = aiResponse.match(/```json\n([\s\S]*?)\n```/);
        if (jsonMatch && jsonMatch[1]) {
            aiResponse = jsonMatch[1].trim();
        }

        // Попытка распарсить JSON ответ
        if (aiResponse === 'null' || aiResponse.toLowerCase() === 'null' || aiResponse === '') {
            console.log(`  - OpenAI: новость не про сурьму или пустой ответ, пропускаем`);
            return null;
        }

        try {
            const processedNews = JSON.parse(aiResponse);
            console.log(`  - OpenAI: новость обработана успешно`);
            return processedNews;
        } catch (parseError) {
            console.error(`  - OpenAI: ошибка парсинга JSON ответа:`, parseError.message);
            console.error(`  - Ответ OpenAI (сырой):`, response.data.choices[0].message.content.trim());
            console.error(`  - Ответ OpenAI (попытка парсинга):`, aiResponse);
            return null;
        }
    } catch (error) {
        console.error('Error processing news with OpenAI:', error.message);
        if (error.response && error.response.data) {
            console.error('OpenAI API Error details:', error.response.data);
        }
        return null;
    }
}

async function fetchNewsForKeyword(keyword) {
    if (!SCRAPINGDOG_API_KEY) {
        console.error('ScrapingDog API key not set. Skipping news fetch.');
        return [];
    }
    
    const url = 'https://api.scrapingdog.com/google_news/';
    const params = {
        api_key: SCRAPINGDOG_API_KEY,
        query: keyword,
        results: 5,
        page: 0,
        advance_search: "true",
    };
    try {
        console.log(`Fetching news for keyword: "${keyword}" using ScrapingDog...`);
        const response = await axios.get(url, { params: params });
        if (response.status === 200) {
            const data = response.data;
            if (data.news_results && Array.isArray(data.news_results) && data.news_results.length > 0) {
                console.log(`\n--- News for "${keyword}" ---`);
                data.news_results.forEach(newsItem => {
                    console.log(`Title: ${newsItem.title}`);
                    console.log(`Link: ${newsItem.url}`);
                    if (newsItem.source) {
                        console.log(`Source: ${newsItem.source}`);
                    }
                    if (newsItem.date) {
                        console.log(`Date: ${newsItem.lastUpdated}`);
                    }
                    console.log('---');
                });
                // Map news_results to the expected format before passing to processAndSendNews
                const formattedNewsResults = data.news_results.map(item => ({
                    title: item.title,
                    link: item.url, // Use 'url' from API response as 'link'
                    source: item.source,
                    date: item.lastUpdated, // Use 'lastUpdated' from API response as 'date'
                    snippet: item.snippet,
                    thumbnail: item.thumbnail
                }));
                await processAndSendNews(keyword, formattedNewsResults);
            } else {
                console.log(`No news found for keyword: "${keyword}".`);
            }
        } else {
            console.log('Request failed with status code: ' + response.status);
        }
    } catch (error) {
        console.error('Error making the request: ' + error.message);
    }
    // Return empty array in case of error or no results
    return [];
}

// Helper function to check if news is older than 2 days
function isNewsOlderThan2Days(dateString) {
    if (!dateString) return false;

    const now = new Date();
    const twoDaysAgo = new Date(now.getTime() - (2 * 24 * 60 * 60 * 1000)); // 2 days in milliseconds

    // Helper to parse relative dates
    const parseRelativeDate = (str) => {
        const match = str.match(/(\d+)\s*(minute|hour|day|week|month)s?\s*ago/i);
        if (!match) return null;

        const amount = parseInt(match[1]);
        const unit = match[2].toLowerCase();
        let date = new Date(now.getTime());

        switch (unit) {
            case 'minute':
                date.setMinutes(date.getMinutes() - amount);
                break;
            case 'hour':
                date.setHours(date.getHours() - amount);
                break;
            case 'day':
                date.setDate(date.getDate() - amount);
                break;
            case 'week':
                date.setDate(date.getDate() - (amount * 7));
                break;
            case 'month':
                date.setMonth(date.getMonth() - amount);
                break;
            default:
                return null;
        }
        return date;
    };

    try {
        let newsDate;
        if (dateString.includes('ago')) {
            newsDate = parseRelativeDate(dateString);
        } else {
            // Try to parse as a standard date string (e.g., "Jan 8, 2025", "Apr 7, 2025")
            newsDate = new Date(dateString);
        }

        if (newsDate && !isNaN(newsDate.getTime())) {
            return newsDate < twoDaysAgo;
        }

        // If parsing failed, log and return false (assume not old to avoid false positives)
        console.warn(`  - isNewsOlderThan2Days: Не удалось точно распарсить дату "${dateString}". Считаем свежей.`);
        return false;
    } catch (error) {
        console.error(`  - isNewsOlderThan2Days: Ошибка при обработке даты "${dateString}":`, error.message);
        return false;
    }
}

// Test function - временно для проверки
function testDateFiltering() {
    const testDates = [
        "1 day ago",      // должно быть false (свежая)
        "24 hours ago",   // должно быть false (свежая, 1 день)
        "20 hours ago",   // должно быть false (свежая)
        "48 hours ago",   // должно быть true (граница, 2 дня)
        "2 days ago",     // должно быть true (граница)
        "3 days ago",     // должно быть true (старая)
        "6 days ago",    // должно быть true (старая)
        "2 weeks ago",    // должно быть true (старая)
        "1 month ago",    // должно быть true (старая)
        "1 hour ago",     // должно быть false (свежая)
        "12 hours ago",   // должно быть false (свежая)
        "Jan 8, 2025",    // должно быть true (дата в прошлом)
        "June 25, 2025"   // должно быть false (свежая, если сегодня 26 июня 2025)
    ];
    
    console.log("=== Тест фильтрации дат ===");
    testDates.forEach(date => {
        const isOld = isNewsOlderThan2Days(date);
        console.log(`${date}: ${isOld ? 'ПРОПУСТИТЬ (старая)' : 'ОБРАБОТАТЬ (свежая)'}`);
    });
    console.log("=== Конец теста ===\n");
}
async function processAndSendNews(keyword, newsItems) {
    let allNews = [];
    try {
        if (fs.existsSync(NEWS_DATA_FILE_PATH)) {
            const fileData = fs.readFileSync(NEWS_DATA_FILE_PATH, 'utf8');
            if (fileData) {
                allNews = JSON.parse(fileData);
            }
        }
    } catch (err) {
        console.error('Error reading or parsing existing news data file:', err.message);
        // Continue with an empty array if parsing fails
        allNews = [];
    }

    // Загружаем блэклист обработанных URL
    const blacklist = loadBlacklist();
    console.log(`Loaded blacklist with ${blacklist.size} processed URLs`);

    const fetchedAt = new Date().toISOString();
    
    // Filter out news older than 2 days before processing
    const recentNewsItems = newsItems.filter(item => {
        const isOld = isNewsOlderThan2Days(item.date);
        if (isOld) {
            console.log(`  - Пропущена старая новость (${item.date}): "${item.title}"`);
        }
        return !isOld;
    });
    
    if (recentNewsItems.length < newsItems.length) {
        console.log(`Пропущено ${newsItems.length - recentNewsItems.length} старых новостей для "${keyword}"`);
    }
    
    const newEntries = recentNewsItems.map(item => ({
        keyword: keyword,
        title: item.title,
        link: item.link, // This is already mapped from item.url in fetchNewsForKeyword
        source: item.source ? item.source.name : null, // Ensure source.name is used if source is an object
        date: item.date, // This is already mapped from item.lastUpdated in fetchNewsForKeyword
        snippet: item.snippet,
        thumbnail: item.thumbnail,
        fetchedAt: fetchedAt
    }));

    const existingNewsLinks = new Set(allNews.map(item => item.link));
    const newNewsItems = newEntries.filter(item => !existingNewsLinks.has(item.link));
    const skippedItems = newEntries.filter(item => existingNewsLinks.has(item.link));

    if (skippedItems.length > 0) {
        console.log(`Пропущено ${skippedItems.length} новостей для "${keyword}" - уже есть в истории`);
        skippedItems.forEach(item => {
            console.log(`  - Пропущена: "${item.title}"`);
        });
    }

    // Дополнительно фильтруем по блэклисту обработанных URL
    const unprocessedNewsItems = newNewsItems.filter(item => {
        const isBlacklisted = isInBlacklist(item.link, blacklist);
        if (isBlacklisted) {
            console.log(`  - Пропущена (уже обработана OpenAI): "${item.title}"`);
        }
        return !isBlacklisted;
    });

    const blacklistedCount = newNewsItems.length - unprocessedNewsItems.length;
    if (blacklistedCount > 0) {
        console.log(`Пропущено ${blacklistedCount} новостей для "${keyword}" - уже обработаны OpenAI`);
    }

    if (unprocessedNewsItems.length > 0) {
        console.log(`Found ${unprocessedNewsItems.length} new unprocessed news items for "${keyword}".`);

        // Список для хранения только валидных новостей (прошедших OpenAI фильтрацию)
        const validNewsItems = [];
        let blacklistUpdated = false;
        
        for (const newsItem of unprocessedNewsItems) {
            // Добавляем URL в блэклист независимо от результата обработки OpenAI
            const wasAdded = addToBlacklist(newsItem.link, blacklist);
            if (wasAdded) {
                blacklistUpdated = true;
            }

            // Обрабатываем новость через OpenAI
            const processedNews = await processNewsWithOpenAI({
                url: newsItem.link,
                title: newsItem.title,
                published: newsItem.date,
                source: newsItem.source,
                snippet: newsItem.snippet
            });

            // Если OpenAI вернул null (новость не про сурьму), пропускаем её
            if (!processedNews) {
                console.log(`  - Пропущена новость (не про сурьму): "${newsItem.title}"`);
                continue;
            }

            // Добавляем в список валидных новостей
            validNewsItems.push(newsItem);

            // Отправляем в Telegram только если настроен
            if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHAT_ID) {
                // Формируем сообщение на основе обработанных данных
                let message = `🔥 ${processedNews.title_ru}\n\n`;
                message += `📊 ${processedNews.summary_ru}\n\n`;
                
                if (processedNews.market_analytics) {
                    message += `📈 Аналитика:\n`;
                    if (processedNews.market_analytics.price_trend_14d) {
                        message += `• Тренд 14д: ${processedNews.market_analytics.price_trend_14d}\n`;
                    }
                    if (processedNews.market_analytics.forecast_30d) {
                        message += `• Прогноз 30д: ${processedNews.market_analytics.forecast_30d}\n`;
                    }
                    if (processedNews.market_analytics.supply_impact_t) {
                        message += `• Влияние на предложение: ${processedNews.market_analytics.supply_impact_t}\n`;
                    }
                    message += `\n`;
                }

                if (processedNews['ТРИ_ГЛАЗА']) {
                    const triGlaza = processedNews['ТРИ_ГЛАЗА'];
                    message += `🎯 Ключевые моменты:\n`;
                    if (triGlaza.risk && triGlaza.risk.length > 0) {
                        message += `⚠️ Риски: ${triGlaza.risk.join('; ')}\n`;
                    }
                    if (triGlaza.opportunity && triGlaza.opportunity.length > 0) {
                        message += `💰 Возможности: ${triGlaza.opportunity.join('; ')}\n`;
                    }
                    message += `\n`;
                }

                if (processedNews.ASIM_short_insight) {
                    message += `🧠 Инсайт: ${processedNews.ASIM_short_insight}\n\n`;
                }

                message += `🔗 ${newsItem.link}\n`;
                message += `📅 ${processedNews.pub_time || newsItem.date || 'N/A'}\n`;
                message += `📰 ${processedNews.source || newsItem.source || 'N/A'}`;

                if (processedNews.notification_level === 'CRITICAL') {
                    message = `🚨 КРИТИЧНО! 🚨\n\n${message}`;
                }

                await sendTelegramMessage(TELEGRAM_CHAT_ID, message);
                // Add a small delay between Telegram messages to avoid hitting rate limits
                await new Promise(resolve => setTimeout(resolve, 1000));
            } else {
                console.log(`  - Валидная новость (про сурьму): "${newsItem.title}"`);
            }
        }
        
        // Сохраняем обновленный блэклист
        if (blacklistUpdated) {
            saveBlacklist(blacklist);
        }
        
        // Сохраняем только валидные новости (прошедшие OpenAI фильтрацию)
        if (validNewsItems.length > 0) {
            allNews.push(...validNewsItems);
            try {
                fs.writeFileSync(NEWS_DATA_FILE_PATH, JSON.stringify(allNews, null, 2), 'utf8');
                console.log(`Successfully saved ${validNewsItems.length} valid news items for "${keyword}" to ${NEWS_DATA_FILE_PATH}`);
            } catch (err) {
                console.error('Error writing news data to file:', err.message);
            }
        } else {
            console.log(`No valid news items found for "${keyword}" after OpenAI filtering.`);
        }
    } else {
        console.log(`No new unprocessed news items found for "${keyword}".`);
    }
}


async function processKeywords() {
    try {
        const keywordsData = fs.readFileSync(KEYWORDS_FILE_PATH, 'utf8');
        const keywords = keywordsData.split(/\r?\n/).map(k => k.trim()).filter(k => k.length > 0); // Split by newline, trim, filter empty

        if (keywords.length === 0) {
            console.log('No keywords found in .env_keys file.');
            return;
        }

        console.log(`Found keywords: ${keywords.join(', ')}`);

        for (const keyword of keywords) {
            await fetchNewsForKeyword(keyword);
            // Add a small delay between requests to be polite to the API
            await new Promise(resolve => setTimeout(resolve, 1000)); 
        }
    } catch (error) {
        console.error('Error reading or processing keywords file:', error.message);
    }
}

async function runDailyTask() {
    console.log(`\nStarting news check cycle at ${new Date().toISOString()}`);
    
    // Временный тест фильтрации дат
    testDateFiltering();
    
    await processKeywords();
    console.log(`News check cycle finished. Next check in 24 hours.`);
    setTimeout(runDailyTask, CHECK_INTERVAL_MS);
}

// Start the first cycle
if (!OPENAI_API_KEY) {
    console.error('OpenAI API key is not set. News filtering will be disabled.');
}

if (!SCRAPINGDOG_API_KEY) {
    console.error('ScrapingDog API key is not set. News fetching will be disabled.');
}

if (!fs.existsSync(PROMPT_FILE_PATH)) {
    console.error('Prompt file (.env_prompt) not found. AI processing may use fallback prompt.');
} else {
    console.log('Prompt file loaded successfully.');
}

if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
    console.warn('Telegram BOT_TOKEN or CHAT_ID is not set. News will be fetched and saved, but not sent to Telegram.');
    console.log('News Alert script started. Initial check will run now.');
    runDailyTask();
}
else {
    console.log('News Alert script started. Initial check will run now.');
    console.log(`Telegram Bot Token loaded successfully: ${TELEGRAM_BOT_TOKEN.substring(0, 5)}...`);
    console.log(`Telegram Chat ID loaded successfully: ${TELEGRAM_CHAT_ID}`);
    if (OPENAI_API_KEY) {
        console.log(`OpenAI API key loaded successfully: ${OPENAI_API_KEY.substring(0, 5)}...`);
    }
    if (SCRAPINGDOG_API_KEY) {
        console.log(`ScrapingDog API key loaded successfully: ${SCRAPINGDOG_API_KEY.substring(0, 5)}...`);
    }
    
    // Запускаем только если не в тестовой среде
    if (process.env.NODE_ENV !== 'test') {
        runDailyTask();
    }
}

// Экспорт функций для тестирования
module.exports = {
    isNewsOlderThan2Days,
    processNewsWithOpenAI,
    sendTelegramMessage,
    fetchNewsForKeyword,
    filterNewsByDate,
    filterNewsByKeywords,
    loadPromptFromFile,
    loadKeywordsFromFile,
    fetchNewsFromSerpApi: fetchNewsForKeyword, // alias
    fetchNewsFromScrapingDog: fetchNewsForKeyword, // alias  
    sendTelegramNotification: sendTelegramMessage,
    loadBlacklist,
    saveBlacklist,
    addToBlacklist,
    isInBlacklist
};

// Utility functions for filtering and processing
function filterNewsByDate(newsItems, daysBack = 1) {
  if (!newsItems || !Array.isArray(newsItems)) {
    return [];
  }
  
  const cutoffTime = Date.now() - (daysBack * 24 * 60 * 60 * 1000);
  
  return newsItems.filter(item => {
    if (!item || !item.published) {
      return false;
    }
    
    try {
      const publishedTime = new Date(item.published).getTime();
      return publishedTime >= cutoffTime && !isNaN(publishedTime);
    } catch (error) {
      return false;
    }
  });
}

function filterNewsByKeywords(newsItems, keywords) {
  if (!newsItems || !Array.isArray(newsItems)) {
    return [];
  }
  
  if (!keywords || !Array.isArray(keywords) || keywords.length === 0) {
    return [];
  }
  
  return newsItems.filter(item => {
    if (!item) {
      return false;
    }
    
    const title = (item.title || '').toLowerCase();
    const html = (item.html || '').toLowerCase();
    const content = title + ' ' + html;
    
    return keywords.some(keyword => 
      content.includes(keyword.toLowerCase())
    );
  });
}

function loadKeywordsFromFile() {
  try {
    if (fs.existsSync(KEYWORDS_FILE_PATH)) {
      const keywordsContent = fs.readFileSync(KEYWORDS_FILE_PATH, 'utf8');
      return keywordsContent.split('\n').filter(line => line.trim());
    }
  } catch (error) {
    console.log('Error loading keywords file:', error.message);
  }
  
  // Default keywords
  return ['antimony', 'trioxide', 'sb2o3', 'antimony oxide'];
}

function loadPromptFromFile() {
  try {
    if (fs.existsSync(PROMPT_FILE_PATH)) {
      return fs.readFileSync(PROMPT_FILE_PATH, 'utf8');
    }
  } catch (error) {
    console.log('Error loading prompt file:', error.message);
  }
  
  // Fallback prompt
  return `Analyze this news item about Sb₂O₃ (Antimony Trioxide): {{NEWS_DATA}}
Please provide a brief summary focusing on market impact.`;
}

// Функции для работы с блэклистом обработанных URL
function loadBlacklist() {
    try {
        if (fs.existsSync(BLACKLIST_FILE_PATH)) {
            const blacklistData = fs.readFileSync(BLACKLIST_FILE_PATH, 'utf8');
            const blacklist = JSON.parse(blacklistData);
            return new Set(blacklist.urls || []);
        }
    } catch (error) {
        console.error('Error loading blacklist:', error.message);
    }
    return new Set();
}

function saveBlacklist(blacklistSet) {
    try {
        const blacklistData = {
            lastUpdated: new Date().toISOString(),
            count: blacklistSet.size,
            urls: Array.from(blacklistSet)
        };
        fs.writeFileSync(BLACKLIST_FILE_PATH, JSON.stringify(blacklistData, null, 2), 'utf8');
        console.log(`Blacklist updated: ${blacklistSet.size} processed URLs`);
    } catch (error) {
        console.error('Error saving blacklist:', error.message);
    }
}

function addToBlacklist(url, blacklistSet) {
    if (url && !blacklistSet.has(url)) {
        blacklistSet.add(url);
        console.log(`  - Added to blacklist: ${url}`);
        return true;
    }
    return false;
}

function isInBlacklist(url, blacklistSet) {
    return blacklistSet.has(url);
}
