const logger = require('../../src/utils/logger');
const winston = require('winston');

// Mock winston
jest.mock('winston', () => {
  const mockLogger = {
    info: jest.fn(),
    error: jest.fn(),
    warn: jest.fn(),
    debug: jest.fn(),
    add: jest.fn()
  };

  return {
    createLogger: jest.fn(() => mockLogger),
    format: {
      combine: jest.fn(),
      timestamp: jest.fn(),
      errors: jest.fn(),
      json: jest.fn(),
      colorize: jest.fn(),
      simple: jest.fn()
    },
    transports: {
      File: jest.fn(),
      Console: jest.fn()
    }
  };
});

describe('Logger', () => {
  let mockLogger;

  beforeEach(() => {
    jest.clearAllMocks();
    mockLogger = winston.createLogger();
  });

  test('should create logger with correct configuration', () => {
    expect(winston.createLogger).toHaveBeenCalledWith({
      level: process.env.LOG_LEVEL || 'info',
      format: undefined, // Mocked
      defaultMeta: { service: 'yandex-direct-service' },
      transports: [
        expect.any(winston.transports.File), // error.log
        expect.any(winston.transports.File)  // combined.log
      ]
    });
  });

  test('should add console transport in non-production environment', () => {
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'development';
    
    // Re-require the logger to trigger the environment check
    delete require.cache[require.resolve('../../src/utils/logger')];
    require('../../src/utils/logger');
    
    expect(mockLogger.add).toHaveBeenCalledWith(expect.any(winston.transports.Console));
    
    process.env.NODE_ENV = originalEnv;
  });

  test('should not add console transport in production environment', () => {
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'production';
    
    // Re-require the logger to trigger the environment check
    delete require.cache[require.resolve('../../src/utils/logger')];
    require('../../src/utils/logger');
    
    expect(mockLogger.add).not.toHaveBeenCalled();
    
    process.env.NODE_ENV = originalEnv;
  });

  test('should use custom log level from environment', () => {
    const originalLevel = process.env.LOG_LEVEL;
    process.env.LOG_LEVEL = 'debug';
    
    // Re-require the logger to trigger the environment check
    delete require.cache[require.resolve('../../src/utils/logger')];
    require('../../src/utils/logger');
    
    expect(winston.createLogger).toHaveBeenCalledWith(
      expect.objectContaining({
        level: 'debug'
      })
    );
    
    process.env.LOG_LEVEL = originalLevel;
  });

  test('should configure file transports correctly', () => {
    expect(winston.transports.File).toHaveBeenCalledWith({
      filename: 'logs/error.log',
      level: 'error'
    });
    
    expect(winston.transports.File).toHaveBeenCalledWith({
      filename: 'logs/combined.log'
    });
  });

  test('should configure format correctly', () => {
    expect(winston.format.combine).toHaveBeenCalled();
    expect(winston.format.timestamp).toHaveBeenCalledWith({
      format: 'YYYY-MM-DD HH:mm:ss'
    });
    expect(winston.format.errors).toHaveBeenCalledWith({ stack: true });
    expect(winston.format.json).toHaveBeenCalled();
  });
});
