const { RLP } = require('@ethereumjs/rlp');

// Простой тест RLP кодирования/декодирования
console.log('Testing simple RLP encoding/decoding...');

const testData = {
  height: 0,
  timestamp: 1234567890,
  inputs: []
};

console.log('Original data:', testData);

// Сериализация для RLP
function serializeForRLP(obj) {
  if (obj === null || obj === undefined) {
    return null;
  }
  if (typeof obj === 'bigint') {
    return obj.toString();
  }
  if (obj instanceof Map) {
    // Convert Map to an array of [key, value] pairs, ensuring deterministic order
    const sortedEntries = Array.from(obj.entries()).sort((a, b) => a[0].localeCompare(b[0]));
    return sortedEntries.map(([key, value]) => [serializeForRLP(key), serializeForRLP(value)]);
  }
  if (Array.isArray(obj)) {
    return obj.map(item => serializeForRLP(item));
  }
  if (typeof obj === 'object' && obj.constructor === Object) {
    // Convert plain objects to an array of [key, value] pairs
    // Sort keys to ensure deterministic RLP encoding
    const sortedKeys = Object.keys(obj).sort();
    return sortedKeys.map(key => [key, serializeForRLP(obj[key])]);
  }
  if (Buffer.isBuffer(obj)) {
    return new Uint8Array(obj);
  }
  return obj;
}

const serialized = serializeForRLP(testData);
console.log('Serialized data:', JSON.stringify(serialized, null, 2));

const encoded = RLP.encode(serialized);
console.log('RLP encoded type:', encoded.constructor.name);
console.log('RLP encoded length:', encoded.length);
console.log('RLP encoded (hex):', Buffer.from(encoded).toString('hex'));

const decoded = RLP.decode(encoded);
console.log('RLP decoded:', decoded);

// Тест с более сложными данными
console.log('\n--- Testing complex data ---');

const complexData = {
  height: 0,
  timestamp: Date.now(),
  inputs: [[
    [{
      type: 'proposal',
      data: {
        map: new Map([['a', 1n], ['b', 2n]]),
        bigint: 12345678901234567890n,
        buffer: Buffer.from('hello'),
      }
    }],
    { someEntityState: 'data' }
  ]]
};

console.log('Complex data inputs structure:', JSON.stringify(complexData.inputs, (key, value) => {
  if (value instanceof Map) {
    return Array.from(value.entries());
  }
  if (typeof value === 'bigint') {
    return value.toString() + 'n';
  }
  if (Buffer.isBuffer(value)) {
    return value.toString();
  }
  return value;
}, 2));

try {
  const complexSerialized = serializeForRLP(complexData);
  console.log('Complex serialized structure length:', JSON.stringify(complexSerialized).length);
  
  const complexEncoded = RLP.encode(complexSerialized);
  console.log('Complex RLP encoded length:', complexEncoded.length);
  console.log('Complex RLP encoded (first 100 bytes as hex):', Buffer.from(complexEncoded).subarray(0, 100).toString('hex'));
  
  const complexDecoded = RLP.decode(complexEncoded);
  console.log('Complex RLP decode success!');
  console.log('Decoded length:', complexDecoded.length);
} catch (error) {
  console.error('Complex RLP error:', error);
}
