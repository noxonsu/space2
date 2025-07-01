// Глобальная настройка для тестов
require('dotenv').config({ path: '.env.test' });

// Мокаем winston logger для тестов
jest.mock('../src/utils/logger', () => ({
  info: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  debug: jest.fn()
}));

// Настройка timeout для длительных тестов
jest.setTimeout(30000);

// Глобальные переменные для тестов
global.TEST_TIMEOUT = 10000;
global.LONG_TEST_TIMEOUT = 30000;
