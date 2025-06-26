const {
  filterNewsByDate,
  filterNewsByKeywords,
  processNewsWithOpenAI,
  loadPromptFromFile
} = require('../space2_newsalert');

describe('Integration Tests - News Processing Pipeline', () => {
  // Mock news data for testing
  const mockNewsItems = [
    {
      url: 'https://example.com/sb2o3-news',
      title: 'Antimony trioxide prices surge in China',
      html: '<p>Antimony trioxide (Sb2O3) prices increased by 15% this week...</p>',
      published: new Date().toISOString(),
      source: 'ChemNews',
      lang: 'en'
    },
    {
      url: 'https://example.com/other-news',
      title: 'General chemical industry news',
      html: '<p>Various chemical updates...</p>',
      published: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
      source: 'Industry Today',
      lang: 'en'
    }
  ];

  test('Full pipeline: date filtering -> keyword filtering -> AI processing', async () => {
    // Step 1: Filter by date (last 24 hours)
    const recentNews = filterNewsByDate(mockNewsItems, 1);
    expect(recentNews).toHaveLength(1);
    expect(recentNews[0].title).toContain('Antimony trioxide');

    // Step 2: Filter by keywords
    const relevantNews = filterNewsByKeywords(recentNews, ['antimony', 'trioxide', 'sb2o3']);
    expect(relevantNews).toHaveLength(1);

    // Step 3: AI processing would happen here (mocked in other tests)
    expect(relevantNews[0]).toHaveProperty('url');
    expect(relevantNews[0]).toHaveProperty('title');
    expect(relevantNews[0]).toHaveProperty('html');
  });

  test('Pipeline handles empty news array', () => {
    const result = filterNewsByDate([], 1);
    expect(result).toEqual([]);
    
    const keywordResult = filterNewsByKeywords([], ['antimony']);
    expect(keywordResult).toEqual([]);
  });

  test('Pipeline handles news with missing fields', () => {
    const incompleteNews = [
      { title: 'Test news' }, // missing other fields
      { url: 'http://example.com' }, // missing other fields
    ];

    const dateFiltered = filterNewsByDate(incompleteNews, 1);
    expect(dateFiltered).toEqual([]); // Should filter out incomplete items

    const keywordFiltered = filterNewsByKeywords(incompleteNews, ['test']);
    expect(keywordFiltered).toHaveLength(1); // Should find one match based on title
  });

  test('Prompt loading and validation', () => {
    const prompt = loadPromptFromFile();
    expect(prompt).toBeDefined();
    expect(prompt).toContain('{{NEWS_DATA}}');
    expect(prompt).toContain('Sb₂O₃');
    expect(prompt).toContain('NAMAGIRI');
  });

  test('News data structure validation', () => {
    const validNewsItem = mockNewsItems[0];
    
    // Check required fields for AI processing
    expect(validNewsItem).toHaveProperty('url');
    expect(validNewsItem).toHaveProperty('title');
    expect(validNewsItem).toHaveProperty('html');
    expect(validNewsItem).toHaveProperty('published');
    expect(validNewsItem).toHaveProperty('source');
    
    // Validate ISO date format
    expect(() => new Date(validNewsItem.published)).not.toThrow();
    expect(new Date(validNewsItem.published).toISOString()).toBe(validNewsItem.published);
  });
});
