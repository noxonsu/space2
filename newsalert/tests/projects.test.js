const request = require('supertest');
const http = require('http');
const path = require('path');
const fs = require('fs');

// Mock fs.promises to control file system operations
jest.mock('fs', () => ({
  ...jest.requireActual('fs'), // Import and retain default behavior
  promises: {
    ...jest.requireActual('fs').promises, // Import and retain default behavior for promises
    readFile: jest.fn(),
    writeFile: jest.fn(),
    stat: jest.fn(() => ({ mtime: { getTime: () => Date.now() } })), // Mock stat for newsCache
  },
  existsSync: jest.fn(() => true), // Mock existsSync to always return true for simplicity in tests
}));

// Mock the entire space2_newsalert.js module to control its behavior
let server;
let mockProjectsData = [];

describe('Projects API Endpoints', () => {
  beforeAll(() => {
    // Dynamically require the main app file after mocks are set up
    const appModule = require('../space2_newsalert');
    server = appModule.server; // Assuming the http server is exported as 'server'
  });

  beforeEach(() => {
    // Reset mock data and fs mocks before each test
    mockProjectsData = [];
    fs.promises.readFile.mockClear();
    fs.promises.writeFile.mockClear();
    fs.existsSync.mockClear();

    // Default mock implementations
    fs.promises.readFile.mockImplementation((filePath) => {
      if (filePath.includes('projects.json')) {
        return Promise.resolve(JSON.stringify(mockProjectsData));
      }
      if (filePath.includes('fetched_news.json')) {
        return Promise.resolve(JSON.stringify([])); // Return empty news for project tests
      }
      return Promise.reject(new Error(`File not found: ${filePath}`));
    });
    fs.promises.writeFile.mockImplementation((filePath, data) => {
      if (filePath.includes('projects.json')) {
        mockProjectsData = JSON.parse(data);
        return Promise.resolve();
      }
      return Promise.reject(new Error(`Cannot write to file: ${filePath}`));
    });
    fs.existsSync.mockReturnValue(true); // Assume files exist by default
  });

  afterAll((done) => {
    // Close the server after all tests are done
    if (server && server.listening) {
      server.close(done);
    } else {
      done();
    }
  });

  test('POST /api/projects creates a new project', async () => {
    const newProject = {
      name: 'Test Project',
      keywords: ['test', 'project'],
      prompt: 'Test prompt',
      telegramChatId: '-12345',
      telegramBotToken: 'test_token'
    };

    const response = await request(server)
      .post('/api/projects')
      .send(newProject)
      .expect(201);

    expect(response.body).toMatchObject({
      name: 'Test Project',
      keywords: ['test', 'project'],
      prompt: 'Test prompt',
      telegramChatId: '-12345',
      telegramBotToken: 'test_token'
    });
    expect(response.body).toHaveProperty('id');
    expect(mockProjectsData).toHaveLength(1);
    expect(mockProjectsData[0].name).toBe('Test Project');
  });

  test('GET /api/projects returns all projects', async () => {
    mockProjectsData = [
      { id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA' },
      { id: 'proj_2', name: 'Project B', keywords: ['b'], prompt: 'pB' }
    ];

    const response = await request(server)
      .get('/api/projects')
      .expect(200);

    expect(response.body).toHaveLength(2);
    expect(response.body[0].name).toBe('Project A');
  });

  test('GET /api/projects/:id returns a specific project', async () => {
    mockProjectsData = [
      { id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA' },
      { id: 'proj_2', name: 'Project B', keywords: ['b'], prompt: 'pB' }
    ];

    const response = await request(server)
      .get('/api/projects/proj_1')
      .expect(200);

    expect(response.body.name).toBe('Project A');
  });

  test('GET /api/projects/:id returns 404 if project not found', async () => {
    mockProjectsData = [{ id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA' }];

    await request(server)
      .get('/api/projects/non_existent_id')
      .expect(404);
  });

  test('PUT /api/projects/:id updates an existing project', async () => {
    mockProjectsData = [
      { id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA', telegramChatId: '-123' }
    ];

    const updatedData = {
      name: 'Updated Project A',
      keywords: ['updated'],
      prompt: 'Updated prompt',
      telegramChatId: '-456'
    };

    await request(server)
      .put('/api/projects/proj_1')
      .send(updatedData)
      .expect(200);

    expect(mockProjectsData).toHaveLength(1);
    expect(mockProjectsData[0]).toMatchObject({
      id: 'proj_1',
      name: 'Updated Project A',
      keywords: ['updated'],
      prompt: 'Updated prompt',
      telegramChatId: '-456'
    });
  });

  test('PUT /api/projects/:id updates telegramChatId to undefined if empty string is sent', async () => {
    mockProjectsData = [
      { id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA', telegramChatId: '-123' }
    ];

    const updatedData = {
      name: 'Project A',
      keywords: ['a'],
      prompt: 'pA',
      telegramChatId: '' // Send empty string
    };

    await request(server)
      .put('/api/projects/proj_1')
      .send(updatedData)
      .expect(200);

    expect(mockProjectsData).toHaveLength(1);
    expect(mockProjectsData[0].telegramChatId).toBeUndefined();
  });

  test('PUT /api/projects/:id updates telegramBotToken to undefined if empty string is sent', async () => {
    mockProjectsData = [
      { id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA', telegramBotToken: 'old_token' }
    ];

    const updatedData = {
      name: 'Project A',
      keywords: ['a'],
      prompt: 'pA',
      telegramBotToken: '' // Send empty string
    };

    await request(server)
      .put('/api/projects/proj_1')
      .send(updatedData)
      .expect(200);

    expect(mockProjectsData).toHaveLength(1);
    expect(mockProjectsData[0].telegramBotToken).toBeUndefined();
  });

  test('PUT /api/projects/:id returns 404 if project not found', async () => {
    mockProjectsData = [{ id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA' }];

    await request(server)
      .put('/api/projects/non_existent_id')
      .send({ name: 'New Name' })
      .expect(404);
  });

  test('DELETE /api/projects/:id deletes a project', async () => {
    mockProjectsData = [
      { id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA' },
      { id: 'proj_2', name: 'Project B', keywords: ['b'], prompt: 'pB' }
    ];

    await request(server)
      .delete('/api/projects/proj_1')
      .expect(200);

    expect(mockProjectsData).toHaveLength(1);
    expect(mockProjectsData[0].name).toBe('Project B');
  });

  test('DELETE /api/projects/:id returns 404 if project not found', async () => {
    mockProjectsData = [{ id: 'proj_1', name: 'Project A', keywords: ['a'], prompt: 'pA' }];

    await request(server)
      .delete('/api/projects/non_existent_id')
      .expect(404);
  });
});
