const request = require('supertest');
const express = require('express');

// Mock the main module functions
jest.mock('../space2_newsalert', () => ({
  fetchNewsFromSerpApi: jest.fn(),
  fetchNewsFromScrapingDog: jest.fn(),
  filterNewsByDate: jest.fn(),
  filterNewsByKeywords: jest.fn(),
  processNewsWithOpenAI: jest.fn(),
  sendTelegramNotification: jest.fn(),
  loadPromptFromFile: jest.fn(),
  loadKeywordsFromFile: jest.fn()
}));

const {
  fetchNewsFromSerpApi,
  fetchNewsFromScrapingDog,
  filterNewsByDate,
  filterNewsByKeywords,
  processNewsWithOpenAI,
  sendTelegramNotification,
  loadPromptFromFile,
  loadKeywordsFromFile
} = require('../space2_newsalert');

// Create Express app for testing
const app = express();
app.use(express.json());

// Define routes (normally these would be in the main file)
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.get('/api/config', (req, res) => {
  try {
    const prompt = loadPromptFromFile();
    const keywords = loadKeywordsFromFile();
    res.json({
      promptLoaded: !!prompt,
      keywordsCount: keywords ? keywords.length : 0,
      hasOpenAIKey: !!process.env.OPENAI_API_KEY,
      hasTelegramToken: !!process.env.TELEGRAM_BOT_TOKEN
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/process-news', async (req, res) => {
  try {
    const { newsItems, daysBack = 1 } = req.body;
    
    if (!newsItems || !Array.isArray(newsItems)) {
      return res.status(400).json({ error: 'newsItems must be an array' });
    }

    const keywords = loadKeywordsFromFile();
    const dateFiltered = filterNewsByDate(newsItems, daysBack);
    const keywordFiltered = filterNewsByKeywords(dateFiltered, keywords);
    
    const processedNews = [];
    for (const item of keywordFiltered) {
      const processed = await processNewsWithOpenAI(item);
      processedNews.push(processed);
    }

    res.json({
      totalInput: newsItems.length,
      afterDateFilter: dateFiltered.length,
      afterKeywordFilter: keywordFiltered.length,
      processed: processedNews.length,
      results: processedNews
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

describe('API Endpoints Tests', () => {
  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();
  });

  test('GET /health returns OK status', async () => {
    const response = await request(app)
      .get('/health')
      .expect(200);

    expect(response.body).toHaveProperty('status', 'OK');
    expect(response.body).toHaveProperty('timestamp');
  });

  test('GET /api/config returns configuration status', async () => {
    loadPromptFromFile.mockReturnValue('mocked prompt with {{NEWS_DATA}}');
    loadKeywordsFromFile.mockReturnValue(['antimony', 'trioxide', 'sb2o3']);

    const response = await request(app)
      .get('/api/config')
      .expect(200);

    expect(response.body).toMatchObject({
      promptLoaded: true,
      keywordsCount: 3,
      hasOpenAIKey: expect.any(Boolean),
      hasTelegramToken: expect.any(Boolean)
    });
  });

  test('POST /api/process-news processes news items correctly', async () => {
    const mockNewsItems = [
      {
        url: 'https://example.com/news1',
        title: 'Antimony trioxide market update',
        html: '<p>Market news...</p>',
        published: new Date().toISOString(),
        source: 'ChemNews'
      }
    ];

    loadKeywordsFromFile.mockReturnValue(['antimony', 'trioxide']);
    filterNewsByDate.mockReturnValue(mockNewsItems);
    filterNewsByKeywords.mockReturnValue(mockNewsItems);
    processNewsWithOpenAI.mockResolvedValue({
      ...mockNewsItems[0],
      aiSummary: 'AI generated summary'
    });

    const response = await request(app)
      .post('/api/process-news')
      .send({ newsItems: mockNewsItems, daysBack: 1 })
      .expect(200);

    expect(response.body).toMatchObject({
      totalInput: 1,
      afterDateFilter: 1,
      afterKeywordFilter: 1,
      processed: 1
    });

    expect(response.body.results).toHaveLength(1);
    expect(filterNewsByDate).toHaveBeenCalledWith(mockNewsItems, 1);
    expect(filterNewsByKeywords).toHaveBeenCalledWith(mockNewsItems, ['antimony', 'trioxide']);
    expect(processNewsWithOpenAI).toHaveBeenCalledWith(mockNewsItems[0]);
  });

  test('POST /api/process-news validates input', async () => {
    const response = await request(app)
      .post('/api/process-news')
      .send({ newsItems: 'invalid' })
      .expect(400);

    expect(response.body).toHaveProperty('error', 'newsItems must be an array');
  });

  test('POST /api/process-news handles empty news array', async () => {
    loadKeywordsFromFile.mockReturnValue(['antimony']);
    filterNewsByDate.mockReturnValue([]);
    filterNewsByKeywords.mockReturnValue([]);

    const response = await request(app)
      .post('/api/process-news')
      .send({ newsItems: [] })
      .expect(200);

    expect(response.body).toMatchObject({
      totalInput: 0,
      afterDateFilter: 0,
      afterKeywordFilter: 0,
      processed: 0,
      results: []
    });
  });

  test('API handles configuration loading errors', async () => {
    loadPromptFromFile.mockImplementation(() => {
      throw new Error('Prompt file not found');
    });

    const response = await request(app)
      .get('/api/config')
      .expect(500);

    expect(response.body).toHaveProperty('error', 'Prompt file not found');
  });
});
