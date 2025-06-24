require('dotenv').config({ path: __dirname + '/.env' });
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const express = require('express'); // Add express

const KEYWORDS_FILE_PATH = path.join(__dirname, '.env_keys');
const NEWS_DATA_FILE_PATH = path.join(__dirname, 'fetched_news.json');
const SERPAPI_API_KEY = process.env.SERPAPI_KEY;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;
const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000; // 24 hours

// --- Admin Panel Code ---
const app = express();
const adminPort = 3656; // Use a different variable name for clarity

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoint to get keywords
app.get('/api/keywords', (req, res) => {
  fs.readFile(KEYWORDS_FILE_PATH, 'utf8', (err, data) => { // Use KEYWORDS_FILE_PATH
    if (err) {
      console.error('Error reading keywords file:', err);
      return res.status(500).send('Error reading keywords');
    }
    const keywords = data.split(/\r?\n/).map(line => line.trim()).filter(Boolean); // Use updated split logic
    res.json(keywords);
  });
});

// API endpoint to add a keyword
app.post('/api/keywords', (req, res) => {
  const { keyword } = req.body;
  if (!keyword) {
    return res.status(400).send('Keyword is required');
  }
  fs.appendFile(KEYWORDS_FILE_PATH, `\n${keyword}`, (err) => { // Use KEYWORDS_FILE_PATH, correct newline
    if (err) {
      console.error('Error adding keyword:', err);
      return res.status(500).send('Error adding keyword');
    }
    res.status(201).send('Keyword added');
  });
});

// API endpoint to delete a keyword
app.delete('/api/keywords/:keyword', (req, res) => {
  const keywordToDelete = req.params.keyword;
  fs.readFile(KEYWORDS_FILE_PATH, 'utf8', (err, data) => { // Use KEYWORDS_FILE_PATH
    if (err) {
      console.error('Error reading keywords file:', err);
      return res.status(500).send('Error reading keywords');
    }
    const keywords = data.split(/\r?\n/).map(line => line.trim()).filter(Boolean); // Use updated split logic
    const newKeywords = keywords.filter(k => k !== keywordToDelete);
    const newData = newKeywords.join('\n'); // Correct newline
    fs.writeFile(KEYWORDS_FILE_PATH, newData, 'utf8', (err) => { // Use KEYWORDS_FILE_PATH
      if (err) {
        console.error('Error deleting keyword:', err);
        return res.status(500).send('Error deleting keyword');
      }
      res.send('Keyword deleted');
    });
  });
});

app.listen(adminPort, () => { // Use adminPort
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
        results: 10,
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
