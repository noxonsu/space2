// k/jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['<rootDir>/tests/**/*.test.ts'],
  testSequencer: '<rootDir>/jest.sequencer.js', // Custom test sequencer
  moduleFileExtensions: ['ts', 'js', 'json', 'node'],
  globalSetup: './jest.setup.ts', // Add global setup for cleanup
};
