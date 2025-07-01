require('dotenv').config({ path: __dirname + '/.env' });
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');

const NEWS_DATA_FILE_PATH = path.join(__dirname, 'fetched_news.json');
const PROJECTS_FILE_PATH = path.join(__dirname, 'projects.json');
const BLACKLIST_FILE_PATH = path.join(__dirname, 'processed_urls_blacklist.json');

const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000; // 24 hours

async function fetchScrapingDogCredits() {
    try {
        const apiKey = process.env.SCRAPINGDOG_API_KEY;
        console.log('Fetching ScrapingDog credits with API key:', apiKey ? `${apiKey.substring(0, 8)}...` : 'NOT SET');
        if (!apiKey) {
            console.warn('SCRAPINGDOG_API_KEY is not set. Skipping credits check.');
            return null;
        }
        
        console.log('Making request to ScrapingDog API...');
        const response = await axios.get('https://api.scrapingdog.com/account', {
            params: {
                api_key: apiKey
            }
        });
        
        console.log('ScrapingDog API response status:', response.status);
        console.log('ScrapingDog API response data:', response.data);
        
        return response.data;
    } catch (error) {
        console.error('Error fetching ScrapingDog credits:', error.message);
        if (error.response) {
            console.error('Response status:', error.response.status);
            console.error('Response data:', error.response.data);
        }
        return null;
    }
}

/**
 * Loads news from the local JSON file.
 * @returns {Array} The loaded news articles.
 */
async function loadNewsData() {
    try {
        const fileData = await fs.promises.readFile(NEWS_DATA_FILE_PATH, 'utf8');
        return JSON.parse(fileData);
    } catch (err) {
        if (err.code === 'ENOENT') {
            console.log('News data file not found, returning empty array.');
            return [];
        } else {
            console.error('Error reading or parsing news data file:', err.message);
            throw err;
        }
    }
}

// --- Admin Panel Code ---
const adminPort = 3656;

// --- Cache for news data ---
let newsCache = {
    data: null,
    lastModified: null
};

async function loadProjects() {
    try {
        const projectsData = await fs.promises.readFile(PROJECTS_FILE_PATH, 'utf8');
        return JSON.parse(projectsData);
    } catch (err) {
        if (err.code === 'ENOENT') {
            console.log('Projects file not found, returning empty array.');
            return [];
        } else {
            console.error('Error reading or parsing projects file:', err.message);
            throw err;
        }
    }
}

async function saveProjects(projects) {
    try {
        await fs.promises.writeFile(PROJECTS_FILE_PATH, JSON.stringify(projects, null, 2), 'utf8');
        console.log('Projects saved successfully.');
    } catch (err) {
        console.error('Error saving projects file:', err.message);
        throw err;
    }
}

async function getNewsData(projectId = null) {
    try {
        const stats = await fs.promises.stat(NEWS_DATA_FILE_PATH);
        const lastModified = stats.mtime.getTime();

        if (newsCache.lastModified && newsCache.lastModified === lastModified) {
            console.log('Serving news from cache.');
            let news = newsCache.data;
            if (projectId) {
                news = news.filter(item => item.projectId === projectId);
            }
            return news;
        }

        console.log('Reading and caching news file.');
        const fileData = await fs.promises.readFile(NEWS_DATA_FILE_PATH, 'utf8');
        const newsData = JSON.parse(fileData);
        
        newsCache.data = newsData;
        newsCache.lastModified = lastModified;

        let news = newsData;
        if (projectId) {
            news = news.filter(item => item.projectId === projectId);
        }
        return news;
    } catch (err) {
        if (err.code === 'ENOENT') {
            console.log('News data file not found, returning empty array.');
            return [];
        } else {
            console.error('Error reading or parsing news data file:', err.message);
            throw err;
        }
    }
}

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
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
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
  } else if (pathname === '/api/projects' && method === 'GET') {
    loadProjects()
      .then(projects => {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(projects));
      })
      .catch(err => {
        console.error('Error getting projects:', err);
        res.writeHead(500);
        res.end('Error reading projects');
      });
  } else if (pathname === '/api/projects' && method === 'POST') {
    parseBody(req, (err, newProject) => {
      if (err || !newProject || !newProject.name || !newProject.keywords || !newProject.prompt) {
        res.writeHead(400);
        res.end('Project name, keywords, and prompt are required');
        return;
      }
      loadProjects()
        .then(projects => {
          newProject.id = `proj_${Date.now()}`; // Simple unique ID
          // Ensure telegramBotToken is saved if provided
          if (newProject.telegramBotToken === '') newProject.telegramBotToken = undefined; // Store as undefined if empty string
          projects.push(newProject);
          return saveProjects(projects);
        })
        .then(() => {
          res.writeHead(201, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(newProject));
        })
        .catch(err => {
          console.error('Error creating project:', err);
          res.writeHead(500);
          res.end('Error creating project');
        });
    });
  } else if (pathname.startsWith('/api/projects/') && pathname.endsWith('/news') && method === 'GET') { // <-- Перемещено выше
    const projectId = pathname.split('/')[3];
    getNewsData(projectId)
      .then(newsData => {
        let filteredData = [...newsData];
        const keyword = parsedUrl.query.keyword;
        const status = parsedUrl.query.status;
        
        if (keyword) {
          console.log(`Запрошены новости по ключевому слову: "${keyword}" для проекта ${projectId}`);
          filteredData = filteredData.filter(item => item.keyword === keyword);
        }
        
        if (status) {
          console.log(`Запрошены новости по статусу: "${status}" для проекта ${projectId}`);
          filteredData = filteredData.filter(item => item.status === status);
        }
        
        if (!keyword && !status) {
          console.log(`Запрошены все новости для проекта ${projectId}.`);
        }
        
        filteredData.sort((a, b) => new Date(b.fetchedAt) - new Date(a.fetchedAt));
        const sanitizedNewsData = filteredData.map(item => ({
            ...item,
            link: item.link || '',
            ai_response: item.ai_response || {}
        }));

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(sanitizedNewsData));
      })
      .catch(err => {
        console.error('Error getting news data for project:', err);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify([]));
      });
  } else if (pathname.startsWith('/api/projects/') && method === 'GET') { // <-- Теперь этот маршрут будет обрабатывать только /api/projects/:id
    const projectId = pathname.split('/')[3];
    loadProjects()
      .then(projects => {
        const project = projects.find(p => p.id === projectId);
        if (project) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(project));
        } else {
          res.writeHead(404);
          res.end('Project not found');
        }
      })
      .catch(err => {
        console.error('Error getting project:', err);
        res.writeHead(500);
        res.end('Error reading project');
      });
  } else if (pathname.startsWith('/api/projects/') && method === 'PUT') {
    const projectId = pathname.split('/')[3];
    parseBody(req, (err, updatedProject) => {
      if (err || !updatedProject) {
        res.writeHead(400);
        res.end('Invalid project data');
        return;
      }
      loadProjects()
        .then(projects => {
          const index = projects.findIndex(p => p.id === projectId);
          if (index !== -1) {
            // Ensure telegramBotToken is saved if provided
            if (updatedProject.telegramBotToken === '') updatedProject.telegramBotToken = undefined; // Store as undefined if empty string
            projects[index] = { ...projects[index], ...updatedProject, id: projectId }; // Ensure ID is not changed
            return saveProjects(projects);
          } else {
            res.writeHead(404);
            res.end('Project not found');
            return Promise.reject('Project not found'); // Propagate error
          }
        })
        .then(() => {
          res.writeHead(200);
          res.end('Project updated');
        })
        .catch(err => {
          console.error('Error updating project:', err);
          res.writeHead(500);
          res.end('Error updating project');
        });
    });
  } else if (pathname.startsWith('/api/projects/') && method === 'DELETE') {
    const projectId = pathname.split('/')[3];
    loadProjects()
      .then(projects => {
        const initialLength = projects.length;
        const newProjects = projects.filter(p => p.id !== projectId);
        if (newProjects.length < initialLength) {
          return saveProjects(newProjects);
        } else {
          res.writeHead(404);
          res.end('Project not found');
          return Promise.reject('Project not found');
        }
      })
      .then(() => {
        res.writeHead(200);
        res.end('Project deleted');
      })
      .catch(err => {
        console.error('Error deleting project:', err);
        res.writeHead(500);
        res.end('Error deleting project');
      });
  } else if (pathname === '/api/scrapingdog-credits' && method === 'GET') {
    fetchScrapingDogCredits()
      .then(credits => {
        if (credits) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(credits));
        } else {
          res.writeHead(500);
          res.end('Failed to fetch ScrapingDog credits');
        }
      })
      .catch(err => {
        console.error('Error fetching ScrapingDog credits:', err);
        res.writeHead(500);
        res.end('Error fetching ScrapingDog credits');
      });
  }
  else {
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


async function sendTelegramMessage(chatId, text, telegramBotToken) {
    const url = `https://api.telegram.org/bot${telegramBotToken}/sendMessage`;
    try {
        await axios.post(url, {
            chat_id: chatId,
            text: text,
            disable_web_page_preview: true
        });
        console.log('Telegram message sent successfully.');
    } catch (error) {
        console.error('Error sending Telegram message:', error.message);
        if (error.response && error.response.data) {
            console.error('Telegram API Error details:', error.response.data);
        }
    }
}

async function processNewsWithOpenAI(newsItem, promptTemplate, openaiApiKey) {
    if (!openaiApiKey) {
        console.error('OpenAI API key not set. Skipping AI processing.');
        return null;
    }

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
                'Authorization': `Bearer ${openaiApiKey}`,
                'Content-Type': 'application/json'
            }
        });

        let aiResponse = response.data.choices[0].message.content.trim();
        
        const jsonMatch = aiResponse.match(/```json\n([\s\S]*?)\n```/);
        if (jsonMatch && jsonMatch[1]) {
            aiResponse = jsonMatch[1].trim();
        }

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

async function fetchNewsForKeyword(keyword, scrapingDogApiKey) {
    if (!scrapingDogApiKey) {
        console.error('ScrapingDog API key not set. Skipping news fetch.');
        return [];
    }
    
    const url = 'https://api.scrapingdog.com/google_news/';
    const params = {
        api_key: scrapingDogApiKey,
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
                const formattedNewsResults = data.news_results.map(item => ({
                    title: item.title,
                    link: item.url,
                    source: item.source,
                    date: item.lastUpdated,
                    snippet: item.snippet,
                    thumbnail: item.thumbnail
                }));
                return formattedNewsResults; // Return news items to be processed by the caller
            } else {
                console.log(`No news found for keyword: "${keyword}".`);
            }
        } else {
            console.log('Request failed with status code: ' + response.status);
        }
    } catch (error) {
        console.error('Error making the request: ' + error.message);
    }
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
async function processAndSendNews(projectId, keyword, newsItems, telegramChatId, telegramBotToken, promptTemplate, openaiApiKey) {
    let allNews = [];
    try {
        if (fs.existsSync(NEWS_DATA_FILE_PATH)) {
            const fileData = await fs.promises.readFile(NEWS_DATA_FILE_PATH, 'utf8');
            if (fileData) {
                allNews = JSON.parse(fileData);
            }
        }
    } catch (err) {
        console.error('Error reading or parsing existing news data file:', err.message);
        allNews = [];
    }

    const blacklist = loadBlacklist();
    console.log(`Loaded blacklist with ${blacklist.size} processed URLs`);

    const fetchedAt = new Date().toISOString();
    
    const newsToSave = []; // Будем собирать все новости, которые нужно сохранить

    for (const item of newsItems) {
        const baseNewsItem = {
            projectId: projectId,
            keyword: keyword,
            title: item.title,
            link: item.link,
            source: item.source ? item.source.name : null,
            date: item.date,
            snippet: item.snippet,
            thumbnail: item.thumbnail,
            fetchedAt: fetchedAt,
            status: 'fetched' // Начальный статус
        };

        // Проверка на старые новости
        const isOld = isNewsOlderThan2Days(item.date);
        if (isOld) {
            console.log(`  - Пропущена старая новость (${item.date}): "${item.title}"`);
            newsToSave.push({ ...baseNewsItem, status: 'skipped_old' });
            continue;
        }

        // Проверка на дубликаты (уже есть в fetched_news.json)
        const isExisting = allNews.some(existingItem => existingItem.link === item.link);
        if (isExisting) {
            console.log(`  - Пропущена (уже есть в истории): "${item.title}"`);
            newsToSave.push({ ...baseNewsItem, status: 'skipped_duplicate' });
            continue;
        }

        // Проверка на блэклист (уже обработана OpenAI)
        const isBlacklisted = isInBlacklist(item.link, blacklist);
        if (isBlacklisted) {
            console.log(`  - Пропущена (уже обработана OpenAI): "${item.title}"`);
            newsToSave.push({ ...baseNewsItem, status: 'skipped_blacklisted' });
            continue;
        }

        // Если новость прошла все фильтры, отправляем в OpenAI
        const processedNews = await processNewsWithOpenAI({
            url: item.link,
            title: item.title,
            published: item.date,
            source: item.source,
            snippet: item.snippet
        }, promptTemplate, openaiApiKey);

        if (!processedNews) {
            console.log(`  - Пропущена новость (не про сурьму): "${item.title}"`);
            newsToSave.push({ ...baseNewsItem, status: 'skipped_irrelevant' });
            continue;
        }

        // Если OpenAI обработал, добавляем в блэклист и сохраняем
        addToBlacklist(item.link, blacklist); // Добавляем в блэклист только после успешной обработки OpenAI
        newsToSave.push({ ...baseNewsItem, ai_response: processedNews, status: 'processed' });

        // Отправка в Telegram
        if (telegramBotToken && telegramChatId) {
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

            message += `🔗 ${item.link}\n`;
            message += `📅 ${processedNews.pub_time || item.date || 'N/A'}\n`;
            message += `📰 ${processedNews.source || item.source || 'N/A'}`;

            if (processedNews.notification_level === 'CRITICAL') {
                message = `🚨 КРИТИЧНО! 🚨\n\n${message}`;
            }

            await sendTelegramMessage(telegramChatId, message, telegramBotToken);
            await new Promise(resolve => setTimeout(resolve, 1000));
        } else {
            console.log(`  - Валидная новость (про сурьму): "${item.title}"`);
        }
    }
    
    saveBlacklist(blacklist); // Сохраняем блэклист после всех операций

    if (newsToSave.length > 0) {
        allNews.push(...newsToSave);
        try {
            await fs.promises.writeFile(NEWS_DATA_FILE_PATH, JSON.stringify(allNews, null, 2), 'utf8');
            console.log(`Successfully saved ${newsToSave.length} news items to ${NEWS_DATA_FILE_PATH}`);
        } catch (err) {
            console.error('Error writing news data to file:', err.message);
        }
    } else {
        console.log(`No new news items to save.`);
    }
}

// ... (unchanged code below)

async function processProjects() {
    const projects = await loadProjects();
    if (projects.length === 0) {
        console.log('No projects found in projects.json.');
        return;
    }

    console.log(`Found ${projects.length} projects.`);

    for (const project of projects) {
        console.log(`\n--- Processing project: "${project.name}" (ID: ${project.id}) ---`);
        // Destructure telegramBotToken from project and handle different ScrapingDog key field names
        const { id, name, telegramChatId, keywords, prompt, openaiApiKey, telegramBotToken } = project;
        
        // Handle different field names for ScrapingDog API key and fallback to environment variable
        const scrapingDogApiKey = project.scrapingDogApiKey || project.scrapingDogKey || process.env.SCRAPINGDOG_API_KEY;

        if (!keywords || keywords.length === 0) {
            console.warn(`Project "${name}" has no keywords. Skipping news fetch.`);
            continue;
        }
        if (!prompt) {
            console.warn(`Project "${name}" has no prompt. Skipping AI processing.`);
            continue;
        }

        for (const keyword of keywords) {
            const newsItems = await fetchNewsForKeyword(keyword, scrapingDogApiKey);
            if (newsItems.length > 0) {
                // Передаем project-specific telegramBotToken
                await processAndSendNews(id, keyword, newsItems, telegramChatId, telegramBotToken, prompt, openaiApiKey);
            }
            await new Promise(resolve => setTimeout(resolve, 1000)); // Задержка между запросами по ключевым словам
        }
    }
}

async function runDailyTask() {
    console.log(`\nStarting news check cycle at ${new Date().toISOString()}`);
    testDateFiltering(); // Keep for now, can be removed later
    await processProjects();
    console.log(`News check cycle finished. Next check in 24 hours.`);
    setTimeout(runDailyTask, CHECK_INTERVAL_MS);
}

// Initial startup logic
console.log('News Alert script started.');
if (process.env.NODE_ENV !== 'test') {
    runDailyTask();
}

// Export functions for testing
module.exports = {
    isNewsOlderThan2Days,
    processNewsWithOpenAI,
    sendTelegramMessage,
    fetchNewsForKeyword,
    filterNewsByDate,
    filterNewsByKeywords,
    loadProjects,
    saveProjects,
    fetchScrapingDogCredits,
    loadBlacklist,
    saveBlacklist,
    addToBlacklist,
    isInBlacklist,
    // Expose for initial project creation logic if needed in tests
    KEYWORDS_FILE_PATH: path.join(__dirname, '.env_keys'), // Re-add for manual migration
    PROMPT_FILE_PATH: path.join(__dirname, '.env_prompt') // Re-add for manual migration
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
