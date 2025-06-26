/// <reference types="node" />
import { glob } from 'glob';
import * as path from 'path';
import * as fs from 'fs';

const dbDir = path.join(__dirname, 'tests', 'integration');

module.exports = async () => {
  const lockFilePath = path.join(dbDir, 'test-db-*-LOCK');
  const lockFiles = await glob(lockFilePath);

  if (lockFiles.length > 0) {
    console.warn(`\nWarning: Found LevelDB lock files from previous test runs:`);
    lockFiles.forEach(file => console.warn(`- ${file}`));
    console.warn(`Please manually remove these files before running tests again.`);
    // throw new Error('LevelDB lock files found. Please clean up manually.'); // Закомментировано, чтобы не блокировать выполнение
  }
};
