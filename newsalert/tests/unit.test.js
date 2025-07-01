
const {
    isNewsOlderThan2Days,
    processNewsWithOpenAI,
    sendTelegramMessage,
    fetchNewsForKeyword,
    loadProjects,
    saveProjects,
    loadBlacklist,
    saveBlacklist,
    addToBlacklist,
    isInBlacklist
} = require('../space2_newsalert');

const fs = require('fs').promises;
const path = require('path');

// Mocking external dependencies
jest.mock('axios');
const axios = require('axios');

// Mocking fs promises
jest.mock('fs', () => ({
    ...jest.requireActual('fs'),
    promises: {
        readFile: jest.fn(),
        writeFile: jest.fn(),
        stat: jest.fn(),
    },
    existsSync: jest.fn(),
}));


describe('News Alert Script - Unit Tests', () => {

    beforeEach(() => {
        // Clear all mocks before each test
        jest.clearAllMocks();
        // Mock console to prevent logs from cluttering test output
        jest.spyOn(console, 'log').mockImplementation(() => {});
        jest.spyOn(console, 'warn').mockImplementation(() => {});
        jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    describe('isNewsOlderThan2Days', () => {
        it('should return true for dates older than 2 days', () => {
            const oldDate = new Date();
            oldDate.setDate(oldDate.getDate() - 3);
            expect(isNewsOlderThan2Days(oldDate.toISOString())).toBe(true);
        });

        it('should return false for dates within the last 2 days', () => {
            const newDate = new Date();
            newDate.setDate(newDate.getDate() - 1);
            expect(isNewsOlderThan2Days(newDate.toISOString())).toBe(false);
        });

        it('should handle relative date strings correctly', () => {
            expect(isNewsOlderThan2Days('3 days ago')).toBe(true);
            expect(isNewsOlderThan2Days('1 day ago')).toBe(false);
            expect(isNewsOlderThan2Days('48 hours ago')).toBe(true);
            expect(isNewsOlderThan2Days('24 hours ago')).toBe(false);
        });
    });

    describe('Blacklist Functions', () => {
        it('should add a URL to the blacklist', () => {
            const blacklist = new Set();
            const url = 'http://example.com/news1';
            const result = addToBlacklist(url, blacklist);
            expect(result).toBe(true);
            expect(blacklist.has(url)).toBe(true);
        });

        it('should not add a duplicate URL to the blacklist', () => {
            const url = 'http://example.com/news1';
            const blacklist = new Set([url]);
            const result = addToBlacklist(url, blacklist);
            expect(result).toBe(false);
        });

        it('should check if a URL is in the blacklist', () => {
            const url = 'http://example.com/news1';
            const blacklist = new Set([url]);
            expect(isInBlacklist(url, blacklist)).toBe(true);
            expect(isInBlacklist('http://example.com/news2', blacklist)).toBe(false);
        });
    });

    describe('processNewsWithOpenAI', () => {
        it('should return null if OpenAI API key is not provided', async () => {
            const result = await processNewsWithOpenAI({}, 'prompt', null);
            expect(result).toBeNull();
        });

        it('should call OpenAI API and return processed news', async () => {
            const newsItem = { title: 'Test News', link: 'http://example.com' };
            const prompt = 'Test prompt';
            const apiKey = 'test-api-key';
            const aiResponse = { summary: 'Test summary' };

            axios.post.mockResolvedValue({
                data: {
                    choices: [{ message: { content: JSON.stringify(aiResponse) } }]
                }
            });

            const result = await processNewsWithOpenAI(newsItem, prompt, apiKey);
            expect(axios.post).toHaveBeenCalledWith(
                'https://api.openai.com/v1/chat/completions',
                expect.any(Object),
                expect.any(Object)
            );
            expect(result).toEqual(aiResponse);
        });

         it('should return null if OpenAI returns a null string', async () => {
            axios.post.mockResolvedValue({
                data: {
                    choices: [{ message: { content: 'null' } }]
                }
            });
            const result = await processNewsWithOpenAI({}, 'prompt', 'api-key');
            expect(result).toBeNull();
        });
    });

    describe('fetchNewsForKeyword', () => {
        it('should return empty array if ScrapingDog API key is not provided', async () => {
            const result = await fetchNewsForKeyword('keyword', null);
            expect(result).toEqual([]);
        });

        it('should call ScrapingDog API and return formatted news', async () => {
            const keyword = 'antimony';
            const apiKey = 'scraping-dog-api-key';
            const apiResponse = {
                news_results: [
                    { title: 'News 1', url: 'http://a.com', source: 'Source A', lastUpdated: '2025-01-01', snippet: 'Snippet A' }
                ]
            };

            axios.get.mockResolvedValue({ status: 200, data: apiResponse });

            const result = await fetchNewsForKeyword(keyword, apiKey);
            expect(axios.get).toHaveBeenCalledWith(
                'https://api.scrapingdog.com/google_news/',
                expect.any(Object)
            );
            expect(result).toEqual([
                { title: 'News 1', link: 'http://a.com', source: 'Source A', date: '2025-01-01', snippet: 'Snippet A', thumbnail: undefined }
            ]);
        });
    });

});
