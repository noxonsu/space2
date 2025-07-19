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

        return newsData; // Возвращаем все новости, фильтрация будет на клиенте
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
  } else if (pathname.startsWith('/api/projects/') && pathname.endsWith('/news') && method === 'GET') {
    // Удаляем projectId из вызова getNewsData, чтобы получить все новости
    getNewsData()
      .then(newsData => {
        const projectId = pathname.split('/')[3]; // Получаем projectId из URL
        let filteredData = newsData.filter(item => item.projectId === projectId); // Фильтруем по projectId на сервере

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
            // Ensure telegramBotToken and telegramChatId are saved if provided, or undefined if empty string
            if (updatedProject.telegramBotToken === '') updatedProject.telegramBotToken = undefined;
            if (updatedProject.telegramChatId === '') updatedProject.telegramChatId = undefined;
            projects[index] = { ...projects[index], ...updatedProject, id: projectId }; // Ensure ID is not changed
            return saveProjects(projects)
              .then(() => {
                res.writeHead(200);
                res.end('Project updated');
              })
              .catch(err => {
                console.error('Error saving updated project:', err);
                res.writeHead(500);
                res.end('Error updating project');
              });
          } else {
            res.writeHead(404);
            res.end('Project not found');
          }
        })
        .catch(err => {
          console.error('Error loading projects for update:', err);
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
          return saveProjects(newProjects)
            .then(() => {
              res.writeHead(200);
              res.end('Project deleted');
            })
            .catch(err => {
              console.error('Error saving projects after deletion:', err);
              res.writeHead(500);
              res.end('Error deleting project');
            });
        } else {
          res.writeHead(404);
          res.end('Project not found');
        }
      })
      .catch(err => {
        console.error('Error loading projects for deletion:', err);
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
  } else if (pathname.startsWith('/api/projects/') && pathname.endsWith('/parse') && method === 'POST') {
    // Запуск парсинга для конкретного проекта
    const projectId = pathname.split('/')[3];
    
    console.log(`🚀 Запуск парсинга для проекта: ${projectId}`);
    
    // Запускаем парсинг асинхронно
    triggerProjectParsing(projectId) // Changed to triggerProjectParsing
      .then(() => {
        console.log(`✅ Парсинг для проекта ${projectId} завершен`);
      })
      .catch(err => {
        console.error(`❌ Ошибка парсинга для проекта ${projectId}:`, err);
      });
    
    // Сразу отвечаем, что парсинг запущен
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      success: true, 
      message: `Парсинг для проекта ${projectId} запущен`,
      projectId: projectId,
      timestamp: new Date().toISOString()
    }));
  } else if (pathname === '/api/parse-projects' && method === 'GET') {
    const projectId = parsedUrl.query.projectId;
    
    console.log(`🚀 Запрос на запуск парсинга: ${projectId ? `проекта ID: ${projectId}` : 'всех проектов'}`);
    
    // Запускаем парсинг асинхронно
    if (projectId) {
      triggerProjectParsing(projectId)
        .then(() => {
          console.log(`✅ Парсинг для проекта ${projectId} завершен`);
        })
        .catch(err => {
          console.error(`❌ Ошибка парсинга для проекта ${projectId}:`, err);
        });
    } else {
      processProjects()
        .then(() => {
          console.log(`✅ Парсинг всех проектов завершен`);
        })
        .catch(err => {
          console.error(`❌ Ошибка парсинга всех проектов:`, err);
        });
    }
    
    // Сразу отвечаем, что парсинг запущен
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      success: true, 
      message: `Парсинг ${projectId ? `проекта ${projectId}` : 'всех проектов'} запущен`,
      projectId: projectId || 'all',
      timestamp: new Date().toISOString()
    }));
  }
  else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// --- End Admin Panel Code ---

// Запускаем сервер только если не в тестовой среде
if (process.env.NODE_ENV !== 'test') {
  server.listen(adminPort, '0.0.0.0', () => { // Bind to 0.0.0.0
    console.log(`Админ панель запущена на порту ${adminPort}`);
    console.log(`Admin panel listening at http://0.0.0.0:${adminPort}`);
  });
}

/**
 * Triggers parsing for a specific project and updates its lastParsedAt timestamp.
 * @param {string} projectId The ID of the project to parse.
 */
async function triggerProjectParsing(projectId) {
    try {
        const projects = await loadProjects();
        const projectIndex = projects.findIndex(p => p.id === projectId);

        if (projectIndex === -1) {
            console.error(`Project with ID "${projectId}" not found.`);
            return { success: false, message: 'Project not found' };
        }

        const project = projects[projectIndex];
        const { name, telegramChatId, keywords, prompt, openaiApiKey, telegramBotToken } = project;
        const scrapingDogApiKey = project.scrapingDogApiKey || project.scrapingDogKey || process.env.SCRAPINGDOG_API_KEY;
        const projectOpenaiApiKey = openaiApiKey || process.env.OPENAI_API_KEY;

        if (!keywords || keywords.length === 0) {
            console.warn(`Project "${name}" has no keywords. Skipping news fetch.`);
            return { success: false, message: 'Project has no keywords' };
        }
        if (!prompt) {
            console.warn(`Project "${name}" has no prompt. Skipping AI processing.`);
            return { success: false, message: 'Project has no prompt' };
        }

        console.log(`\n--- Manually triggering parsing for project: "${name}" (ID: ${projectId}) ---`);
        console.log(`📝 Загружен промпт длиной: ${prompt ? prompt.length : 0} символов`);
        console.log(`🔑 Первые 200 символов промпта: ${prompt ? prompt.substring(0, 200) : 'НЕТ ПРОМПТА'}...`);

        let allProcessedNewsCount = 0;
        for (const keyword of keywords) {
            const newsItems = await fetchNewsForKeyword(keyword, scrapingDogApiKey);
            if (newsItems.length > 0) {
                const result = await processAndSendNews(projectId, keyword, newsItems, telegramChatId, telegramBotToken, prompt, projectOpenaiApiKey);
                // Assuming processAndSendNews returns some info about processed items, though it doesn't currently.
                // For now, we just ensure it runs.
                allProcessedNewsCount += newsItems.length; // This is a rough count, not actual processed items.
            }
            await new Promise(resolve => setTimeout(resolve, 1000)); // Delay between keywords
        }

        // Update lastParsedAt
        project.lastParsedAt = new Date().toISOString();
        projects[projectIndex] = project;
        await saveProjects(projects);

        console.log(`Successfully triggered parsing for project "${name}". Last parsed at: ${project.lastParsedAt}`);
        return { success: true, message: `Parsing triggered for ${name}. Processed ${allProcessedNewsCount} items.` };

    } catch (error) {
        console.error(`Error triggering parsing for project ${projectId}:`, error.message);
        return { success: false, message: `Error triggering parsing: ${error.message}` };
    }
}


async function sendTelegramMessage(chatId, text, telegramBotToken) {
    const url = `https://api.telegram.org/bot${telegramBotToken}/sendMessage`;
    
    console.log(`📤 Отправка сообщения в Telegram:`);
    console.log(`   Chat ID: ${chatId}`);
    console.log(`   Длина сообщения: ${text.length} символов`);
    console.log(`   Первые 100 символов: ${text.substring(0, 100)}...`);
    
    try {
        const response = await axios.post(url, {
            chat_id: chatId,
            text: text,
            disable_web_page_preview: true
        });
        
        console.log(`✅ Сообщение успешно отправлено в Telegram (message_id: ${response.data.result.message_id})`);
        return { success: true, data: response.data };
    } catch (error) {
        console.error(`❌ Ошибка отправки сообщения в Telegram:`, error.message);
        let errorDetails = {
            message: error.message,
            responseStatus: error.response ? error.response.status : null,
            responseData: error.response ? error.response.data : null
        };
        console.error('   Детали ошибки Telegram API:', errorDetails.responseData);
        return { success: false, error: errorDetails };
    }
}

async function processNewsWithOpenAI(newsItem, promptTemplate, openaiApiKey) {
    if (!openaiApiKey) {
        console.error('OpenAI API key not set. Skipping AI processing.');
        console.log('Skipping AI processing');
        return { skip: true, raw_response: 'no_openai_key' };
    }

    // Добавляем текст статьи в newsItem если его нет
    let enrichedNewsItem = { ...newsItem };
    
    // Если есть snippet, добавляем его как текст статьи
    if (newsItem.snippet && !enrichedNewsItem.content) {
        enrichedNewsItem.content = newsItem.snippet;
    }

    let prompt = promptTemplate;

    // Если в шаблоне есть {{NEWS_DATA}}, заменяем его.
    // Иначе, добавляем данные новости в конец.
    if (prompt.includes('{{NEWS_DATA}}')) {
        prompt = prompt.replace('{{NEWS_DATA}}', JSON.stringify(enrichedNewsItem, null, 2));
    } else {
        prompt += '\n\n' + JSON.stringify(enrichedNewsItem, null, 2);
    }

    // Извлекаем системный промпт из общего промпта
    const systemPromptMatch = prompt.match(/^(.*?)(?=\n\n## INPUT|\n\nПроанализируй)/s);
    const systemPrompt = systemPromptMatch ? systemPromptMatch[1].trim() : 'Ты — аналитик. Анализируешь новости согласно инструкциям. Возвращаешь JSON в точном формате или слово "skip" если новость не подходит.';
    const userPrompt = prompt.replace(systemPrompt, '').trim();

    try {
        console.log(`Processing news with OpenAI: "${newsItem.title}"`);
        console.log(`  - Системный промпт: ${systemPrompt.substring(0, 100)}...`);
        console.log(`  - Длина полного промпта: ${prompt.length} символов`);
        
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-4o',
            messages: [
                {
                    role: 'system',
                    content: systemPrompt
                },
                {
                    role: 'user',
                    content: userPrompt
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

        // Проверяем, содержит ли ответ слово "skip" (без учета регистра)
        if (aiResponse.toLowerCase().includes('skip')) {
            console.log(`  - OpenAI: новость пропущена, так как содержит слово "skip".`);
            return { skip: true, raw_response: aiResponse };
        }

        // Если ответ пустой или null, пропускаем
        if (!aiResponse || aiResponse.toLowerCase() === 'null') {
            console.log(`  - OpenAI: новость не по теме или пустой ответ, пропускаем.`);
            return { skip: true, raw_response: aiResponse };
        }

        console.log(`  - OpenAI: новость обработана успешно.`);
        return { raw_response: aiResponse }; // Возвращаем сырой ответ
    } catch (error) {
        console.error('Error processing news with OpenAI:', error.message);
        if (error.response && error.response.data) {
            console.error('OpenAI API Error details:', error.response.data);
        }
        return { skip: true, raw_response: `error: ${error.message}` };
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
        console.log(`🤖 Отправляем новость в OpenAI для анализа: "${item.title}"`);
        console.log(`   URL: ${item.link}`);
        console.log(`   Источник: ${item.source?.name || 'N/A'}`);
        
        const aiResult = await processNewsWithOpenAI({
            url: item.link,
            title: item.title,
            published: item.date,
            source: item.source,
            snippet: item.snippet,
            content: item.snippet // Добавляем snippet как content для анализа
        }, promptTemplate, openaiApiKey);

        // Новая логика обработки ответа OpenAI
        if (!aiResult || aiResult.skip) {
            console.log(`- OpenAI пропустил новость (содержит "skip" или произошла ошибка): "${item.title}"`);
            newsToSave.push({ ...baseNewsItem, status: 'skipped_irrelevant', ai_response: aiResult ? aiResult.raw_response : 'no_response' });
            continue;
        }

        const aiResponseText = aiResult.raw_response;

        console.log(`✅ OpenAI успешно обработал новость: "${item.title}"`);
        console.log(`   Сырой ответ OpenAI: ${aiResponseText.substring(0, 100)}...`);

        // Если OpenAI обработал, добавляем в блэклист и сохраняем
        addToBlacklist(item.link, blacklist); // Добавляем в блэклист только после успешной обработки OpenAI
        newsToSave.push({ ...baseNewsItem, ai_response: aiResponseText, status: 'processed' });

        // Отправка в Telegram
        if (telegramBotToken && telegramChatId) {
            let message = aiResponseText; // Отправляем сырой ответ от OpenAI
            
            // Проверяем, содержит ли ответ слово "CRITICAL" для добавления префикса
            if (aiResponseText.toUpperCase().includes('CRITICAL')) {
                message = `🚨🚨🚨 CRITICAL ALERT 🚨🚨🚨\n\n` + message;
            }

            console.log(`📱 Готовим к отправке в Telegram для проекта "${projectId}"`);
            console.log(`   Новость: "${item.title}"`);
            console.log(`   Chat ID: ${telegramChatId}`);

            const telegramResult = await sendTelegramMessage(telegramChatId, message, telegramBotToken);
            if (!telegramResult.success) {
                console.error(`  - Не удалось отправить сообщение в Telegram для проекта "${projectId}". Обновляем статус проекта.`);
                // Обновляем информацию об ошибке в проекте
                const projects = await loadProjects();
                const projectIndex = projects.findIndex(p => p.id === projectId);
                if (projectIndex !== -1) {
                    projects[projectIndex].lastTelegramError = {
                        timestamp: new Date().toISOString(),
                        message: telegramResult.error.message,
                        responseStatus: telegramResult.error.responseStatus,
                        responseData: telegramResult.error.responseData
                    };
                    await saveProjects(projects);
                }
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        } else {
            console.log(`  - Валидная новость (про сурьму): "${item.title}"`);
        }
    }
    
    saveBlacklist(blacklist); // Сохраняем блэклист после всех операций

    // Статистика обработки
    const processed = newsToSave.filter(n => n.status === 'processed').length;
    const skippedOld = newsToSave.filter(n => n.status === 'skipped_old').length;
    const skippedBlacklisted = newsToSave.filter(n => n.status === 'skipped_blacklisted').length;
    const skippedIrrelevant = newsToSave.filter(n => n.status === 'skipped_irrelevant').length;
    
    console.log(`📊 Статистика обработки новостей для проекта "${projectId}":`);
    console.log(`   Обработано и отправлено в Telegram: ${processed}`);
    console.log(`   Пропущено (старые): ${skippedOld}`);
    console.log(`   Пропущено (в чёрном списке): ${skippedBlacklisted}`);
    console.log(`   Пропущено (не по теме): ${skippedIrrelevant}`);
    console.log(`   Всего новостей сохранено: ${newsToSave.length}`);

    if (newsToSave.length > 0) {
        allNews.push(...newsToSave);
        try {
            await fs.promises.writeFile(NEWS_DATA_FILE_PATH, JSON.stringify(allNews, null, 2), 'utf8');
            console.log(`Successfully saved ${newsToSave.length} news items to ${NEWS_DATA_FILE_PATH}`);
        } catch (err) {
            console.error('Error saving news data to file:', err.message);
        }
    } else {
        console.log(`ℹ️ Нет новых новостей для сохранения.`);
    }
}

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
        
        // Handle OpenAI API key with fallback to environment variable
        const projectOpenaiApiKey = openaiApiKey || process.env.OPENAI_API_KEY;
        
        console.log(`Project OpenAI API key: ${projectOpenaiApiKey ? 'SET' : 'NOT SET'}`);
        console.log(`Project ScrapingDog API key: ${scrapingDogApiKey ? 'SET' : 'NOT SET'}`);

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
                await processAndSendNews(id, keyword, newsItems, telegramChatId, telegramBotToken, prompt, projectOpenaiApiKey);
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
    // runDailyTask(); // Закомментировано, чтобы парсинг запускался только по кнопке
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
    server // Export the server instance
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
