// Custom Jest test sequencer to run unit tests before integration tests
const Sequencer = require('@jest/test-sequencer').default;

class CustomSequencer extends Sequencer {
  sort(tests) {
    // Sort tests to run unit tests before integration tests
    const unitTests = tests.filter(test => test.path.includes('/unit/'));
    const integrationTests = tests.filter(test => test.path.includes('/integration/'));
    const otherTests = tests.filter(test => 
      !test.path.includes('/unit/') && !test.path.includes('/integration/')
    );

    // Return in order: unit tests, integration tests, other tests
    return [...unitTests, ...integrationTests, ...otherTests];
  }
}

module.exports = CustomSequencer;
