const {
  filterNewsByDate,
  filterNewsByKeywords,
  loadKeywordsFromFile,
  loadPromptFromFile
} = require('../space2_newsalert');
const fs = require('fs');
const path = require('path');

describe('Utility Functions and Error Handling', () => {
  describe('Date filtering edge cases', () => {
    test('handles invalid date formats gracefully', () => {
      const newsWithInvalidDates = [
        { title: 'News 1', published: 'invalid-date' },
        { title: 'News 2', published: null },
        { title: 'News 3', published: undefined },
        { title: 'News 4', published: '' },
        { title: 'News 5', published: new Date().toISOString() }
      ];

      const result = filterNewsByDate(newsWithInvalidDates, 1);
      expect(result).toHaveLength(1); // Only the valid date should pass
      expect(result[0].title).toBe('News 5');
    });

    test('handles future dates correctly', () => {
      const futureDate = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
      const newsWithFutureDate = [
        { title: 'Future news', published: futureDate }
      ];

      const result = filterNewsByDate(newsWithFutureDate, 1);
      expect(result).toHaveLength(1); // Future dates should be included
    });

    test('handles very old dates', () => {
      const oldDate = new Date('2020-01-01').toISOString();
      const newsWithOldDate = [
        { title: 'Old news', published: oldDate }
      ];

      const result = filterNewsByDate(newsWithOldDate, 1);
      expect(result).toHaveLength(0); // Old dates should be filtered out
    });
  });

  describe('Keyword filtering edge cases', () => {
    test('case insensitive keyword matching', () => {
      const news = [
        { title: 'ANTIMONY TRIOXIDE prices', html: 'content' },
        { title: 'antimony trioxide market', html: 'content' },
        { title: 'Antimony Trioxide industry', html: 'content' },
        { title: 'unrelated news', html: 'content' }
      ];

      const keywords = ['antimony', 'trioxide'];
      const result = filterNewsByKeywords(news, keywords);
      expect(result).toHaveLength(3);
    });

    test('partial keyword matching', () => {
      const news = [
        { title: 'Sb2O3 compound analysis', html: 'content' },
        { title: 'sb2o3 market trends', html: 'content' },
        { title: 'Iron oxide news', html: 'content' }
      ];

      const keywords = ['sb2o3', 'oxide'];
      const result = filterNewsByKeywords(news, keywords);
      expect(result).toHaveLength(3); // All should match due to 'oxide'
    });

    test('handles empty keywords array', () => {
      const news = [{ title: 'Any news', html: 'content' }];
      const result = filterNewsByKeywords(news, []);
      expect(result).toHaveLength(0); // No keywords = no matches
    });

    test('handles news items without title or html', () => {
      const news = [
        { title: 'antimony news' }, // no html
        { html: 'trioxide content' }, // no title
        { url: 'http://example.com' }, // neither title nor html
        { title: 'antimony news', html: 'trioxide content' }
      ];

      const keywords = ['antimony', 'trioxide'];
      const result = filterNewsByKeywords(news, keywords);
      expect(result).toHaveLength(3); // First 3 should match
    });
  });

  describe('File loading functions', () => {
    test('loadKeywordsFromFile handles missing file', () => {
      // Temporarily rename the file to simulate missing file
      const keywordsPath = path.join(__dirname, '../.env_keys');
      const backupPath = path.join(__dirname, '../.env_keys.backup');
      
      let fileRenamed = false;
      if (fs.existsSync(keywordsPath)) {
        fs.renameSync(keywordsPath, backupPath);
        fileRenamed = true;
      }

      try {
        const result = loadKeywordsFromFile();
        // Should return default keywords or handle gracefully
        expect(Array.isArray(result)).toBe(true);
      } finally {
        // Restore the file
        if (fileRenamed) {
          fs.renameSync(backupPath, keywordsPath);
        }
      }
    });

    test('loadPromptFromFile handles missing file', () => {
      // Temporarily rename the file to simulate missing file
      const promptPath = path.join(__dirname, '../.env_prompt');
      const backupPath = path.join(__dirname, '../.env_prompt.backup');
      
      let fileRenamed = false;
      if (fs.existsSync(promptPath)) {
        fs.renameSync(promptPath, backupPath);
        fileRenamed = true;
      }

      try {
        const result = loadPromptFromFile();
        // Should return fallback prompt
        expect(typeof result).toBe('string');
        expect(result.length).toBeGreaterThan(0);
      } finally {
        // Restore the file
        if (fileRenamed) {
          fs.renameSync(backupPath, promptPath);
        }
      }
    });
  });

  describe('Data validation', () => {
    test('validates news item structure', () => {
      const validNewsItem = {
        url: 'https://example.com/news',
        title: 'Test news',
        html: '<p>Content</p>',
        published: new Date().toISOString(),
        source: 'Test Source',
        lang: 'en'
      };

      // Check all required fields are present
      expect(validNewsItem).toHaveProperty('url');
      expect(validNewsItem).toHaveProperty('title');
      expect(validNewsItem).toHaveProperty('html');
      expect(validNewsItem).toHaveProperty('published');
      expect(validNewsItem).toHaveProperty('source');

      // Validate URL format
      expect(validNewsItem.url).toMatch(/^https?:\/\/.+/);

      // Validate date format
      expect(() => new Date(validNewsItem.published)).not.toThrow();
    });

    test('handles malformed news items', () => {
      const malformedItems = [
        null,
        undefined,
        'string instead of object',
        {},
        { url: 'not-a-url' },
        { title: '', html: '', published: 'invalid-date' }
      ];

      malformedItems.forEach(item => {
        // Functions should handle malformed data gracefully
        expect(() => filterNewsByDate([item], 1)).not.toThrow();
        expect(() => filterNewsByKeywords([item], ['test'])).not.toThrow();
      });
    });
  });

  describe('Performance and limits', () => {
    test('handles large datasets efficiently', () => {
      // Create a large dataset
      const largeNewsSet = Array.from({ length: 1000 }, (_, i) => ({
        title: `News item ${i}`,
        html: `Content ${i} with antimony trioxide`,
        published: new Date(Date.now() - i * 60 * 1000).toISOString(), // Spread over time
        url: `https://example.com/news/${i}`,
        source: 'Test Source'
      }));

      const startTime = Date.now();
      const dateFiltered = filterNewsByDate(largeNewsSet, 1);
      const keywordFiltered = filterNewsByKeywords(dateFiltered, ['antimony', 'trioxide']);
      const endTime = Date.now();

      // Should complete in reasonable time (less than 1 second)
      expect(endTime - startTime).toBeLessThan(1000);
      expect(keywordFiltered.length).toBeGreaterThan(0);
    });

    test('handles empty and null inputs', () => {
      expect(() => filterNewsByDate(null, 1)).not.toThrow();
      expect(() => filterNewsByDate(undefined, 1)).not.toThrow();
      expect(() => filterNewsByKeywords(null, ['test'])).not.toThrow();
      expect(() => filterNewsByKeywords([], null)).not.toThrow();
    });
  });
});
