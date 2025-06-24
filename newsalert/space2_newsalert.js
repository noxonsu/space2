require('dotenv').config({ path: __dirname + '/.env' });
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');

const KEYWORDS_FILE_PATH = path.join(__dirname, '.env_keys');
const NEWS_DATA_FILE_PATH = path.join(__dirname, 'fetched_news.json');
const SERPAPI_API_KEY = process.env.SERPAPI_KEY;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;
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

server.listen(adminPort, () => {
  console.log(`Админ панель запущена на порту ${adminPort}`);
  console.log(`Admin panel listening at http://localhost:${adminPort}`);
});
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

async function fetchNewsForKeyword(keyword) {
    const api_key = '6856816ef6fca153ee766fe3';
    const url = 'https://api.scrapingdog.com/google_news/';
    const params = {
        api_key: api_key,
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
                await processAndSendNews(keyword, data.news_results);
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

async function saveNewsToFile(keyword, newsItems) {
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

    const fetchedAt = new Date().toISOString();
    const newEntries = newsItems.map(item => ({
        keyword: keyword,
        title: item.title,
        link: item.link,
        source: item.source ? item.source.name : null,
        date: item.date,
        snippet: item.snippet, // Adding snippet
        thumbnail: item.thumbnail, // Adding thumbnail
        fetchedAt: fetchedAt
    }));

    const existingNewsLinks = new Set(allNews.map(item => item.link));
    const newNewsItems = newEntries.filter(item => !existingNewsLinks.has(item.link));

    if (newNewsItems.length > 0) {
        console.log(`Found ${newNewsItems.length} new news items for "${keyword}".`);
        allNews.push(...newNewsItems);

        try {
            fs.writeFileSync(NEWS_DATA_FILE_PATH, JSON.stringify(allNews, null, 2), 'utf8');
            console.log(`Successfully saved ${newNewsItems.length} new news items for "${keyword}" to ${NEWS_DATA_FILE_PATH}`);
        } catch (err) {
            console.error('Error writing news data to file:', err.message);
        }

        if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
            console.error('Telegram BOT_TOKEN or CHAT_ID is not set. Skipping Telegram notification.');
        } else {
            for (const newsItem of newNewsItems) {
                const message = `Новость по запросу "${newsItem.keyword}":\n\n${newsItem.title}\n${newsItem.link}\n\nИсточник: ${newsItem.source || 'N/A'}\nДата: ${newsItem.date || 'N/A'}`;
                await sendTelegramMessage(TELEGRAM_CHAT_ID, message);
                // Add a small delay between Telegram messages to avoid hitting rate limits
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
    } else {
        console.log(`No new news items found for "${keyword}".`);
    }
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

    const fetchedAt = new Date().toISOString();
    const newEntries = newsItems.map(item => ({
        keyword: keyword,
        title: item.title,
        link: item.link,
        source: item.source || null,
        date: item.date,
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

    if (newNewsItems.length > 0) {
        console.log(`Found ${newNewsItems.length} new news items for "${keyword}".`);
        allNews.push(...newNewsItems);

        try {
            fs.writeFileSync(NEWS_DATA_FILE_PATH, JSON.stringify(allNews, null, 2), 'utf8');
            console.log(`Successfully saved ${newNewsItems.length} new news items for "${keyword}" to ${NEWS_DATA_FILE_PATH}`);
        } catch (err) {
            console.error('Error writing news data to file:', err.message);
        }

        if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
            console.error('Telegram BOT_TOKEN or CHAT_ID is not set. Skipping Telegram notification.');
        } else {
            for (const newsItem of newNewsItems) {
                const message = `Новость по запросу "${newsItem.keyword}":\n\n${newsItem.title}\n${newsItem.url}\n\nИсточник: ${newsItem.source || 'N/A'}\n Дата: ${newsItem.lastUpdated || 'N/A'}`;
                await sendTelegramMessage(TELEGRAM_CHAT_ID, message);
                // Add a small delay between Telegram messages to avoid hitting rate limits
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
    } else {
        console.log(`No new news items found for "${keyword}".`);
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
    await processKeywords();
    console.log(`News check cycle finished. Next check in 24 hours.`);
    setTimeout(runDailyTask, CHECK_INTERVAL_MS);
}

// Start the first cycle
if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
    console.warn('Telegram BOT_TOKEN or CHAT_ID is not set. News will be fetched and saved, but not sent to Telegram.');
    console.log('News Alert script started. Initial check will run now.');
    runDailyTask();
}
else {
    console.log('News Alert script started. Initial check will run now.');
    console.log(`Telegram Bot Token loaded successfully: ${TELEGRAM_BOT_TOKEN.substring(0, 5)}...`);
    console.log(`Telegram Chat ID loaded successfully: ${TELEGRAM_CHAT_ID}`);
    runDailyTask();
}
