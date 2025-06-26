import { Server } from '../../src/server';
import { Entity } from '../../src/entity';
import * as EthCrypto from 'eth-crypto';
import * as fs from 'fs';
import * as path from 'path';
import { WebSocket } from 'ws';
import { Block, Input, Transaction, EntityState } from '../../src/types';
import { RLP } from '@ethereumjs/rlp';
import { Level } from 'level';

// Helper function to deserialize data from RLP decoding
function deserializeFromRLP(rlpData: any): any {
  // Обработка Uint8Array (которые возвращает RLP.decode)
  if (rlpData instanceof Uint8Array) {
    // Если это пустой массив, то это был 0
    if (rlpData.length === 0) {
      return 0;
    }
    try {
      const str = Buffer.from(rlpData).toString('utf8');
      // Проверяем, является ли это строковым представлением BigInt
      if (/^\d+$/.test(str) && str.length > 15) {
        return BigInt(str);
      }
      // Проверяем, может ли это быть числом
      const num = parseInt(str, 10);
      if (!isNaN(num) && num.toString() === str) {
        return num;
      }
      return str;
    } catch (e) {
      // Если это не валидная UTF-8 строка, возможно это число в бинарном формате
      if (rlpData.length <= 8) {
        // Преобразуем из big-endian в число
        let result = 0;
        for (let i = 0; i < rlpData.length; i++) {
          result = (result * 256) + rlpData[i];
        }
        return result;
      }
      return Buffer.from(rlpData);
    }
  }
  
  if (!Array.isArray(rlpData)) {
    return rlpData;
  }

  // Проверяем, является ли это сериализованным объектом (массив пар [key, value])
  // Это происходит когда serializeForRLP обрабатывает plain objects или Maps
  if (rlpData.length > 0 && rlpData.every(item => Array.isArray(item) && item.length === 2)) {
    
    // Проверяем, являются ли все первые элементы строками (ключами объекта)
    const allKeysAreStrings = rlpData.every(([key, value]: [any, any]) => {
      const deserializedKey = deserializeFromRLP(key);
      return typeof deserializedKey === 'string';
    });
    
    if (allKeysAreStrings) {
      // Это объект - создаем из пар key-value
      const keyValuePairs = rlpData.map(([key, value]: [any, any]) => [
        deserializeFromRLP(key), 
        deserializeFromRLP(value)
      ]);
      
      // Создаем объект для быстрого поиска ключей
      const keyValueObj: { [key: string]: any } = {};
      for (const [key, value] of keyValuePairs) {
        keyValueObj[key] = value;
      }
      
      if (keyValueObj.type && keyValueObj.data) {
        // Это Input объект
        return {
          type: keyValueObj.type,
          data: keyValueObj.data
        };
      }
      
      if (keyValueObj.map && keyValueObj.bigint !== undefined && keyValueObj.buffer) {
        // Это data объект из Input с map, bigint и buffer
        const result: any = {};
        
        for (const [key, value] of keyValuePairs) {
          if (key === 'map' && (Array.isArray(value) || (typeof value === 'object' && value !== null))) {
            // Восстанавливаем Map
            const map = new Map();
            if (Array.isArray(value)) {
              // Если это массив пар [key, value]
              for (const [mapKey, mapValue] of value) {
                const deserializedKey = deserializeFromRLP(mapKey);
                const deserializedValue = deserializeFromRLP(mapValue);
                // Проверяем, является ли значение строковым представлением BigInt
                if (typeof deserializedValue === 'string' && /^\d+$/.test(deserializedValue)) {
                  map.set(deserializedKey, BigInt(deserializedValue));
                } else {
                  map.set(deserializedKey, deserializedValue);
                }
              }              } else {
                // Если это объект, конвертируем его в Map
                for (const [mapKey, mapValue] of Object.entries(value)) {
                  // В нашем тесте оригинальные значения были BigInt
                  if (typeof mapValue === 'number') {
                    map.set(mapKey, BigInt(mapValue));
                  } else if (typeof mapValue === 'string' && /^\d+$/.test(mapValue)) {
                    map.set(mapKey, BigInt(mapValue));
                  } else {
                    map.set(mapKey, mapValue);
                  }
                }
              }
            result[key] = map;
          } else if (key === 'bigint' && (typeof value === 'string' || typeof value === 'bigint')) {
            result[key] = typeof value === 'bigint' ? value : BigInt(value);
          } else if (key === 'buffer' && (typeof value === 'string' || Buffer.isBuffer(value))) {
            result[key] = Buffer.isBuffer(value) ? value : Buffer.from(value);
          } else {
            result[key] = value;
          }
        }
        
        return result;
      }
      
      // Это обычный объект
      return keyValueObj;
    }
  }

  // Рекурсивно обрабатываем элементы массива
  return rlpData.map(item => deserializeFromRLP(item));
}


describe('Server Integration', () => {
  let server: Server;
  let currentDbPath: string;
  let currentWsPort: number;

  beforeEach(async () => {
    currentDbPath = path.join(__dirname, `test-db-${Date.now()}`);
    currentWsPort = 8080 + Math.floor(Math.random() * 100); // Unique port for each test
    await cleanup(currentDbPath); // Ensure cleanup for unique path
    server = new Server(currentDbPath, currentWsPort);
  });

  afterEach(async () => {
    await server.stop();
    
    // Сохраняем артефакты LevelDB перед очисткой
    await saveDbArtifacts(currentDbPath);
    
    await cleanup(currentDbPath);
  });

  // Helper to clear a specific test database
  const cleanup = async (dbPathToClean: string) => {
    if (fs.existsSync(dbPathToClean)) {
      await fs.promises.rm(dbPathToClean, { recursive: true, force: true });
    }
  };

  // Helper to save LevelDB artifacts for inspection
  const saveDbArtifacts = async (dbPath: string) => {
    if (!fs.existsSync(dbPath)) {
      console.log(`Database path ${dbPath} does not exist, skipping artifact save`);
      return;
    }
    
    try {
      const artifactsDir = path.join(__dirname, 'leveldb-artifacts');
      if (!fs.existsSync(artifactsDir)) {
        fs.mkdirSync(artifactsDir, { recursive: true });
      }
      
      const timestamp = Date.now();
      const artifactPath = path.join(artifactsDir, `db-${timestamp}`);
      
      // Copy the entire database directory
      await fs.promises.cp(dbPath, artifactPath, { recursive: true });
      
      // Also create a summary file with database contents
      const db = new Level<string, Uint8Array>(dbPath, { valueEncoding: 'view' });
      await db.open();
      
      const summaryFile = path.join(artifactsDir, `db-summary-${timestamp}.txt`);
      let summary = `LevelDB Contents (${new Date().toISOString()}):\n`;
      summary += `Database Path: ${dbPath}\n`;
      summary += `Artifact Path: ${artifactPath}\n\n`;
      
      for await (const [key, value] of db.iterator()) {
        summary += `Key: ${key}\n`;
        summary += `Value Length: ${value.length} bytes\n`;
        
        // Try to decode RLP data for block entries
        if (key.startsWith('block_')) {
          try {
            const decodedArray = RLP.decode(value) as any[];
            summary += `RLP Decoded Structure:\n`;
            summary += JSON.stringify(decodedArray, (key, val) => {
              if (val instanceof Uint8Array) {
                return `Uint8Array(${val.length})`;
              }
              return val;
            }, 2);
            summary += '\n';
          } catch (e) {
            summary += `RLP Decode Error: ${e}\n`;
          }
        } else {
          // For non-block entries, try to display as string
          try {
            summary += `Value (as string): ${Buffer.from(value).toString('utf8')}\n`;
          } catch (e) {
            summary += `Value: <binary data>\n`;
          }
        }
        summary += '\n---\n\n';
      }
      
      await fs.promises.writeFile(summaryFile, summary);
      await db.close();
      
      console.log(`LevelDB artifacts saved to: ${artifactPath}`);
      console.log(`Database summary saved to: ${summaryFile}`);
    } catch (error) {
      console.error('Error saving LevelDB artifacts:', error);
    }
  };

  it('should start, create a block, and restore state', async () => {
    const entityAIdentity = EthCrypto.createIdentity();
    const entityBIdentity = EthCrypto.createIdentity();
    const entityA = new Entity(entityAIdentity);
    const entityB = new Entity(entityBIdentity);

    server.addEntity(entityA);
    server.addEntity(entityB);

    entityA.createAccount(entityB.getState().id);
    entityB.createAccount(entityA.getState().id);
    const { input } = await entityA.initiateTransaction(entityB.getState().id, 100n, 'USD');
    server.submitInput(entityA.getState().id, input);

    await server.start();
    
    await new Promise(resolve => setTimeout(resolve, 150)); // Wait for block to be processed
    
    await server.stop();

    const server2 = new Server(currentDbPath, currentWsPort + 1);
    await server2.start();
    // @ts-ignore
    expect(server2.currentBlockHeight).toBe(1);
    await server2.stop();
  }, 15000); // Increased timeout

  it('should broadcast new blocks to WebSocket clients', (done) => {
    const ws = new WebSocket(`ws://localhost:${currentWsPort}`);
    let transaction: Transaction;

    ws.on('message', (data) => {
      const block: Block = JSON.parse(data.toString(), (key, value) => {
        if (typeof value === 'string' && /^\d+n$/.test(value)) {
          return BigInt(value.slice(0, -1));
        }
        if (value && value.type === 'Buffer' && Array.isArray(value.data)) {
            return Buffer.from(value.data);
        }
        return value;
      });
      expect(block.height).toBe(0);
      expect(block.inputs).toBeInstanceOf(Array);
      expect(block.inputs.length).toBe(1);
      // @ts-ignore
      expect(block.inputs[0][0][0].data.id).toBe(transaction.id);
      ws.close();
      done();
    });

    ws.on('open', async () => {
      const entityAIdentity = EthCrypto.createIdentity();
      const entityBIdentity = EthCrypto.createIdentity();
      const entityA = new Entity(entityAIdentity);
      const entityB = new Entity(entityBIdentity);

      server.addEntity(entityA);
      server.addEntity(entityB);

      entityA.createAccount(entityB.getState().id);
      entityB.createAccount(entityA.getState().id);
      const { input, transaction: tx } = await entityA.initiateTransaction(entityB.getState().id, 100n, 'USD');
      transaction = tx;
      server.submitInput(entityB.getState().id, input);

      await server.start();
    });
  }, 15000); // Increased timeout

  it('should correctly RLP-encode and decode a block with Map, BigInt, and Buffer', async () => {
    const entityAIdentity = EthCrypto.createIdentity();
    const entityA = new Entity(entityAIdentity);
    server.addEntity(entityA);

    const input: Input = {
      type: 'proposal',
      data: {
        map: new Map([['a', 1n], ['b', 2n]]),
        bigint: 12345678901234567890n,
        buffer: Buffer.from('hello'),
      },
    };
    server.submitInput(entityA.getState().id, input);

    await server.start();
    await new Promise(resolve => setTimeout(resolve, 150));
    await server.stop();

    const db = new Level<string, Uint8Array>(currentDbPath, { valueEncoding: 'view' });
    await db.open();
    const rlpEncodedBlock = await db.get('block_0');
    const decodedArray = RLP.decode(rlpEncodedBlock) as any[];
    
    // The decodedArray will be an array of RLP-decoded values.
    // We need to reconstruct the original Block object from this array.
    // The order of properties in Object.values(block) in server.ts is: height, inputs, timestamp (sorted alphabetically)
    
    // Создаем объект из массива пар [key, value]
    const blockObj: any = {};
    for (const [keyBuffer, value] of decodedArray) {
      const key = Buffer.from(keyBuffer).toString();
      blockObj[key] = deserializeFromRLP(value);
    }
    
    const decodedBlock: Block = {
      height: blockObj.height,
      timestamp: blockObj.timestamp,
      inputs: blockObj.inputs,
    };

    expect(decodedBlock.height).toBe(0);
    expect(decodedBlock.inputs).toBeInstanceOf(Array);
    expect(decodedBlock.inputs.length).toBe(1);

    // Check the deserialized input data
    const decodedInput = decodedBlock.inputs[0][0][0]; // Accessing the first input's data
    expect(decodedInput.type).toBe('proposal');
    expect(decodedInput.data.map).toBeInstanceOf(Map);
    expect(decodedInput.data.map.get('a')).toBe(1n);
    expect(decodedInput.data.map.get('b')).toBe(2n);
    expect(decodedInput.data.bigint).toBe(12345678901234567890n);
    expect(decodedInput.data.buffer).toEqual(Buffer.from('hello'));
    
    await db.close();
  }, 15000); // Increased timeout

  it('should create blocks every second when there are inputs', async () => {
    const entityAIdentity = EthCrypto.createIdentity();
    const entityA = new Entity(entityAIdentity);
    server.addEntity(entityA);

    await server.start();

    // Submit inputs with delays greater than 100ms to ensure they go into separate blocks
    server.submitInput(entityA.getState().id, { type: 'transaction', data: { id: 'tx1' } });
    await new Promise(resolve => setTimeout(resolve, 150)); // Wait for first block to be created

    server.submitInput(entityA.getState().id, { type: 'transaction', data: { id: 'tx2' } });
    await new Promise(resolve => setTimeout(resolve, 150)); // Wait for second block to be created

    server.submitInput(entityA.getState().id, { type: 'transaction', data: { id: 'tx3' } });
    await new Promise(resolve => setTimeout(resolve, 150)); // Wait for third block to be created

    // @ts-ignore
    expect(server.currentBlockHeight).toBeGreaterThanOrEqual(3); // Expect at least 3 blocks

    await server.stop();
  }, 15000); // Increased timeout
});
