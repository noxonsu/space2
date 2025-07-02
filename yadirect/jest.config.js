module.exports = {
  testEnvironment: 'node',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/index.js', // Исключаем главный файл сервера
    '!**/node_modules/**'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  testMatch: [
    '**/tests/**/*.test.js'
  ],
  verbose: true,
  // Настройки для разных типов тестов
  projects: [
    {
      displayName: 'unit',
      testMatch: ['**/tests/unit/**/*.test.js'],
      testTimeout: 10000
    },
    {
      displayName: 'integration',
      testMatch: ['**/tests/integration/**/*.test.js'],
      testTimeout: 15000
    },
    {
      displayName: 'e2e',
      testMatch: ['**/tests/e2e/**/*.test.js'],
      testTimeout: 30000
    },
    {
      displayName: 'performance',
      testMatch: ['**/tests/performance/**/*.test.js'],
      testTimeout: 60000
    },
    {
      displayName: 'security',
      testMatch: ['**/tests/security/**/*.test.js'],
      testTimeout: 20000
    }
  ],
  // Глобальные настройки
  maxWorkers: '50%',
  collectCoverage: true,
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50
    }
  }
};
