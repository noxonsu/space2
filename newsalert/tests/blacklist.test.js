const {
  loadBlacklist,
  saveBlacklist,
  addToBlacklist,
  isInBlacklist
} = require('../space2_newsalert');
const fs = require('fs');
const path = require('path');

describe('Blacklist Functionality Tests', () => {
  const testBlacklistPath = path.join(__dirname, '../processed_urls_blacklist.json');
  
  // Cleanup before each test
  beforeEach(() => {
    if (fs.existsSync(testBlacklistPath)) {
      fs.unlinkSync(testBlacklistPath);
    }
  });

  // Cleanup after all tests
  afterAll(() => {
    if (fs.existsSync(testBlacklistPath)) {
      fs.unlinkSync(testBlacklistPath);
    }
  });

  describe('loadBlacklist', () => {
    test('returns empty Set when file does not exist', () => {
      const blacklist = loadBlacklist();
      expect(blacklist).toBeInstanceOf(Set);
      expect(blacklist.size).toBe(0);
    });

    test('loads existing blacklist from file', () => {
      // Create a test blacklist file
      const testData = {
        lastUpdated: new Date().toISOString(),
        count: 2,
        urls: ['https://example.com/news1', 'https://example.com/news2']
      };
      fs.writeFileSync(testBlacklistPath, JSON.stringify(testData, null, 2));

      const blacklist = loadBlacklist();
      expect(blacklist.size).toBe(2);
      expect(blacklist.has('https://example.com/news1')).toBe(true);
      expect(blacklist.has('https://example.com/news2')).toBe(true);
    });

    test('handles corrupted blacklist file gracefully', () => {
      // Create a corrupted file
      fs.writeFileSync(testBlacklistPath, 'invalid json');

      const blacklist = loadBlacklist();
      expect(blacklist).toBeInstanceOf(Set);
      expect(blacklist.size).toBe(0);
    });
  });

  describe('saveBlacklist', () => {
    test('saves blacklist to file correctly', () => {
      const blacklist = new Set(['https://example.com/news1', 'https://example.com/news2']);
      
      saveBlacklist(blacklist);
      
      expect(fs.existsSync(testBlacklistPath)).toBe(true);
      
      const savedData = JSON.parse(fs.readFileSync(testBlacklistPath, 'utf8'));
      expect(savedData.count).toBe(2);
      expect(savedData.urls).toContain('https://example.com/news1');
      expect(savedData.urls).toContain('https://example.com/news2');
      expect(savedData.lastUpdated).toBeDefined();
    });

    test('saves empty blacklist correctly', () => {
      const blacklist = new Set();
      
      saveBlacklist(blacklist);
      
      const savedData = JSON.parse(fs.readFileSync(testBlacklistPath, 'utf8'));
      expect(savedData.count).toBe(0);
      expect(savedData.urls).toEqual([]);
    });
  });

  describe('addToBlacklist', () => {
    test('adds new URL to blacklist', () => {
      const blacklist = new Set();
      const url = 'https://example.com/news1';
      
      const result = addToBlacklist(url, blacklist);
      
      expect(result).toBe(true);
      expect(blacklist.has(url)).toBe(true);
      expect(blacklist.size).toBe(1);
    });

    test('does not add duplicate URL', () => {
      const blacklist = new Set(['https://example.com/news1']);
      const url = 'https://example.com/news1';
      
      const result = addToBlacklist(url, blacklist);
      
      expect(result).toBe(false);
      expect(blacklist.size).toBe(1);
    });

    test('handles null or undefined URL', () => {
      const blacklist = new Set();
      
      const result1 = addToBlacklist(null, blacklist);
      const result2 = addToBlacklist(undefined, blacklist);
      const result3 = addToBlacklist('', blacklist);
      
      expect(result1).toBe(false);
      expect(result2).toBe(false);
      expect(result3).toBe(false);
      expect(blacklist.size).toBe(0);
    });
  });

  describe('isInBlacklist', () => {
    test('returns true for blacklisted URL', () => {
      const blacklist = new Set(['https://example.com/news1']);
      
      expect(isInBlacklist('https://example.com/news1', blacklist)).toBe(true);
    });

    test('returns false for non-blacklisted URL', () => {
      const blacklist = new Set(['https://example.com/news1']);
      
      expect(isInBlacklist('https://example.com/news2', blacklist)).toBe(false);
    });

    test('returns false for empty blacklist', () => {
      const blacklist = new Set();
      
      expect(isInBlacklist('https://example.com/news1', blacklist)).toBe(false);
    });

    test('handles null or undefined URL', () => {
      const blacklist = new Set(['https://example.com/news1']);
      
      expect(isInBlacklist(null, blacklist)).toBe(false);
      expect(isInBlacklist(undefined, blacklist)).toBe(false);
    });
  });

  describe('Integration tests', () => {
    test('full blacklist workflow', () => {
      // Start with empty blacklist
      let blacklist = loadBlacklist();
      expect(blacklist.size).toBe(0);

      // Add some URLs
      const urls = [
        'https://example.com/news1',
        'https://example.com/news2',
        'https://example.com/news3'
      ];

      urls.forEach(url => {
        addToBlacklist(url, blacklist);
      });

      expect(blacklist.size).toBe(3);

      // Save blacklist
      saveBlacklist(blacklist);

      // Load blacklist again
      const reloadedBlacklist = loadBlacklist();
      expect(reloadedBlacklist.size).toBe(3);

      // Check all URLs are present
      urls.forEach(url => {
        expect(isInBlacklist(url, reloadedBlacklist)).toBe(true);
      });

      // Check non-existent URL
      expect(isInBlacklist('https://example.com/news4', reloadedBlacklist)).toBe(false);
    });

    test('blacklist prevents duplicate processing', () => {
      const mockNewsItems = [
        { 
          link: 'https://example.com/news1',
          title: 'Antimony news 1',
          date: new Date().toISOString(),
          source: 'Test Source'
        },
        { 
          link: 'https://example.com/news2',
          title: 'Antimony news 2',
          date: new Date().toISOString(),
          source: 'Test Source'
        },
        { 
          link: 'https://example.com/news1', // Duplicate
          title: 'Antimony news 1 (duplicate)',
          date: new Date().toISOString(),
          source: 'Test Source'
        }
      ];

      // Simulate processing workflow
      const blacklist = loadBlacklist();
      const processedUrls = [];

      mockNewsItems.forEach(item => {
        if (!isInBlacklist(item.link, blacklist)) {
          addToBlacklist(item.link, blacklist);
          processedUrls.push(item.link);
        }
      });

      expect(processedUrls).toHaveLength(2); // Only unique URLs should be processed
      expect(processedUrls).toContain('https://example.com/news1');
      expect(processedUrls).toContain('https://example.com/news2');
      expect(blacklist.size).toBe(2);
    });

    test('blacklist persists between sessions', () => {
      // First session - add URLs
      let blacklist = loadBlacklist();
      addToBlacklist('https://example.com/persistent1', blacklist);
      addToBlacklist('https://example.com/persistent2', blacklist);
      saveBlacklist(blacklist);

      // Simulate new session - load blacklist
      blacklist = loadBlacklist();
      expect(blacklist.size).toBe(2);
      expect(isInBlacklist('https://example.com/persistent1', blacklist)).toBe(true);
      expect(isInBlacklist('https://example.com/persistent2', blacklist)).toBe(true);

      // Add more URLs in second session
      addToBlacklist('https://example.com/persistent3', blacklist);
      saveBlacklist(blacklist);

      // Verify persistence
      blacklist = loadBlacklist();
      expect(blacklist.size).toBe(3);
      expect(isInBlacklist('https://example.com/persistent3', blacklist)).toBe(true);
    });
  });
});
