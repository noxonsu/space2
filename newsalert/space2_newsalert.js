require('dotenv').config({ path: __dirname + '/.env' });
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const KEYWORDS_FILE_PATH = path.join(__dirname, '.env_keys');
const NEWS_DATA_FILE_PATH = path.join(__dirname, 'fetched_news.json');
const SERPAPI_API_KEY = process.env.SERPAPI_KEY;
const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000; // 24 hours

async function fetchNewsForKeyword(keyword) {
    if (!SERPAPI_API_KEY) {
        console.error('Error: SERPAPI_KEY is not defined in the .env file.');
        return []; // Return empty array if no key
    }

    const params = {
        engine: 'google_news',
        q: keyword,
        api_key: SERPAPI_API_KEY,
        hl: 'ru' // Language set to Russian
    };

    try {
        console.log(`Fetching news for keyword: "${keyword}"...`);
        const response = await axios.get('https://serpapi.com/search.json', { params });
        
        if (response.data && response.data.news_results) {
            if (response.data.news_results.length === 0) {
                console.log(`No news found for keyword: "${keyword}".`);
            } else {
                console.log(`\n--- News for "${keyword}" ---`);
                response.data.news_results.forEach(newsItem => {
                    console.log(`Title: ${newsItem.title}`);
                    console.log(`Link: ${newsItem.link}`);
                    if (newsItem.source && newsItem.source.name) {
                        console.log(`Source: ${newsItem.source.name}`);
                    }
                    if (newsItem.date) {
                        console.log(`Date: ${newsItem.date}`);
                    }
                    console.log('---');
                });
                await saveNewsToFile(keyword, response.data.news_results);
            }
        } else {
            console.log(`No news_results found in API response for keyword: "${keyword}".`);
            if (response.data && response.data.search_metadata && response.data.search_metadata.status === 'Error') {
                console.error(`API Error for "${keyword}": ${response.data.search_metadata.error}`);
            } else if (response.data && response.data.error) {
                console.error(`API Error for "${keyword}": ${response.data.error}`);
            }
        }
    } catch (error) {
        console.error(`Error fetching news for keyword "${keyword}":`, error.message);
        if (error.response && error.response.data && error.response.data.error) {
            console.error('API Error details:', error.response.data.error);
        }
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

    // Simple append, could add duplicate checking by link if needed
    allNews.push(...newEntries);

    try {
        fs.writeFileSync(NEWS_DATA_FILE_PATH, JSON.stringify(allNews, null, 2), 'utf8');
        console.log(`Successfully saved ${newEntries.length} news items for "${keyword}" to ${NEWS_DATA_FILE_PATH}`);
    } catch (err) {
        console.error('Error writing news data to file:', err.message);
    }
}

async function processKeywords() {
    try {
        const keywordsData = fs.readFileSync(KEYWORDS_FILE_PATH, 'utf8');
        const keywords = keywordsData.split('\\n').map(k => k.trim()).filter(k => k.length > 0);

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
if (!SERPAPI_API_KEY) {
    console.error('SERPAPI_KEY is not set. Please check your newsalert/.env file.');
    console.error('The script will not run without the API key.');
} else {
    console.log('News Alert script started. Initial check will run now.');
    console.log(`API Key loaded successfully: ${SERPAPI_API_KEY.substring(0, 5)}...`);
    runDailyTask();
}
