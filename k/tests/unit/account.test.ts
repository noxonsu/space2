// k/tests/unit/account.test.ts
import { Account } from '../../src/account';
import { Transaction, Receipt, EntityID } from '../../src/types';
import { signMessage, recoverPublicKey } from '../../src/crypto';
import * as EthCrypto from 'eth-crypto';
import stringify from 'fast-json-stable-stringify';

// Вспомогательная функция для глубокого преобразования BigInt в строку (дубликат из crypto.ts для целей тестирования)
function deepConvertBigIntToString(obj: any): any {
  if (typeof obj === 'bigint') {
    return obj.toString();
  }
  if (typeof obj !== 'object' || obj === null) {
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map(item => deepConvertBigIntToString(item));
  }
  const newObj: { [key: string]: any } = {};
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      newObj[key] = deepConvertBigIntToString(obj[key]);
    }
  }
  return newObj;
}

describe('Account', () => {
  let entityAId: EntityID;
  let entityBId: EntityID;
  let entityAPrivateKey: string;
  let entityBPrivateKey: string;

  beforeAll(() => {
    const identityA = EthCrypto.createIdentity();
    const identityB = EthCrypto.createIdentity();
    entityAPrivateKey = identityA.privateKey;
    entityBPrivateKey = identityB.privateKey;
    // Убедимся, что публичные ключи не сжаты и не имеют префикса '0x'
    entityAId = identityA.publicKey.startsWith('0x') ? identityA.publicKey.substring(2) : identityA.publicKey;
    entityBId = identityB.publicKey.startsWith('0x') ? identityB.publicKey.substring(2) : identityB.publicKey;
    console.log(`ID Сущности A: ${entityAId}`);
    console.log(`ID Сущности B: ${entityBId}`);
  });

  it('должен инициализироваться с нулевыми балансами', () => {
    const account = new Account(entityAId, entityBId);
    const state = account.getState();
    expect(state.balanceA).toBe(0n);
    expect(state.balanceB).toBe(0n);
    expect(state.lastReceipt).toBeNull();
    expect(state.channelId).toBe([entityAId, entityBId].sort().join('-'));
  });

  it('должен применять валидную транзакцию и обновлять балансы', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    // Устанавливаем начальные балансы вручную для тестирования
    (account as any).state.balanceA = initialBalanceA;
    (account as any).state.balanceB = initialBalanceB;

    const tx: Transaction = {
      id: 'tx1',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 10n,
      asset: 'USD',
      nonce: 1,
    };

    const messageToSignForSigning = stringify(deepConvertBigIntToString(tx));
    const messageHashForSigning = EthCrypto.hash.keccak256(messageToSignForSigning);
    console.log('Хеш сообщения для подписи (tx1):', messageHashForSigning);

    const senderSignature = await signMessage(entityAPrivateKey, tx);
    const receiverSignature = await signMessage(entityBPrivateKey, tx);

    const receipt: Receipt = {
      transactionId: tx.id,
      signatures: [senderSignature, receiverSignature],
      timestamp: Date.now(),
      transaction: tx, // Добавляем объект транзакции
    };

    const applied = account.applyTransaction(tx, receipt);
    expect(applied).toBe(true);
    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA - tx.amount);
    expect(state.balanceB).toBe(initialBalanceB + tx.amount);
    expect(state.lastReceipt).toEqual(receipt);
  });

  it('должен отклонять транзакцию с невалидной подписью отправителя', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    (account as any).state.balanceA = initialBalanceA;
    (account as any).state.balanceB = initialBalanceB;

    const tx: Transaction = {
      id: 'tx2',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 10n,
      asset: 'USD',
      nonce: 2,
    };

    const messageToSignForSigning2 = stringify(deepConvertBigIntToString(tx));
    const messageHashForSigning2 = EthCrypto.hash.keccak256(messageToSignForSigning2);
    console.log('Хеш сообщения для подписи (tx2):', messageHashForSigning2);

    // Невалидная подпись (например, от случайного приватного ключа)
    const invalidSignature = await signMessage('0x1234567890123456789012345678901234567890123456789012345678901234', tx);
    const receiverSignature = await signMessage(entityBPrivateKey, tx);

    const receipt: Receipt = {
      transactionId: tx.id,
      signatures: [invalidSignature, receiverSignature],
      timestamp: Date.now(),
      transaction: tx, // Добавляем объект транзакции
    };

    const applied = account.applyTransaction(tx, receipt);
    expect(applied).toBe(false); // Должно быть false из-за невалидной подписи
    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA); // Балансы не должны измениться
    expect(state.balanceB).toBe(initialBalanceB);
    expect(state.lastReceipt).toBeNull(); // Последняя квитанция не должна обновляться
  });

  it('должен отклонять транзакцию с отсутствующей подписью получателя', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    (account as any).state.balanceA = initialBalanceA;
    (account as any).state.balanceB = initialBalanceB;

    const tx: Transaction = {
      id: 'tx3',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 10n,
      asset: 'USD',
      nonce: 3,
    };

    const messageToSignForSigning3 = stringify(deepConvertBigIntToString(tx));
    const messageHashForSigning3 = EthCrypto.hash.keccak256(messageToSignForSigning3);
    console.log('Хеш сообщения для подписи (tx3):', messageHashForSigning3);

    const senderSignature = await signMessage(entityAPrivateKey, tx);

    const receipt: Receipt = {
      transactionId: tx.id,
      signatures: [senderSignature], // Отсутствует подпись получателя
      timestamp: Date.now(),
      transaction: tx, // Добавляем объект транзакции
    };

    const applied = account.applyTransaction(tx, receipt);
    expect(applied).toBe(false);
    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA);
    expect(state.balanceB).toBe(initialBalanceB);
    expect(state.lastReceipt).toBeNull();
  });

  it('должен обрабатывать разрешение конфликта по правилу "правый побеждает" (без изменений, если нет последней квитанции)', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    (account as any).state.balanceA = initialBalanceA;
    (account as any).state.balanceB = initialBalanceB;

    const tx: Transaction = {
      id: 'tx4',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 10n,
      asset: 'USD',
      nonce: 4,
    };

    // Симулируем конфликт без валидной последней квитанции
    account.resolveConflict(tx);

    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA); // Должны остаться без изменений
    expect(state.balanceB).toBe(initialBalanceB);
  });

  it('должен обрабатывать разрешение конфликта по правилу "правый побеждает" (откат к состоянию последней квитанции)', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    (account as any).state.balanceA = initialBalanceA;
    (account as any).state.balanceB = initialBalanceB;

    // Сначала применяем валидную транзакцию, чтобы установить lastReceipt
    const tx1: Transaction = {
      id: 'tx5',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 10n,
      asset: 'USD',
      nonce: 5,
    };
    const messageToSignForSigning5 = stringify(deepConvertBigIntToString(tx1));
    const messageHashForSigning5 = EthCrypto.hash.keccak256(messageToSignForSigning5);
    console.log('Хеш сообщения для подписи (tx5):', messageHashForSigning5);

    const senderSignature1 = await signMessage(entityAPrivateKey, tx1);
    const receiverSignature1 = await signMessage(entityBPrivateKey, tx1);
    const receipt1: Receipt = {
      transactionId: tx1.id,
      signatures: [senderSignature1, receiverSignature1],
      timestamp: Date.now(),
      transaction: tx1, // Добавляем объект транзакции
    };
    account.applyTransaction(tx1, receipt1);

    // Теперь симулируем конфликтующую транзакцию, которая будет невалидной
    const tx2: Transaction = {
      id: 'tx6',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 50n, // Большая сумма, чтобы было очевидно, если применится
      asset: 'USD',
      nonce: 6,
    };
    // Нет валидной квитанции для tx2, или она невалидна
    const invalidReceipt2: Receipt = {
      transactionId: tx2.id,
      signatures: [], // Невалидные подписи
      timestamp: Date.now(),
      transaction: tx2, // Добавляем объект транзакции
    };

    // Вызываем applyTransaction напрямую с невалидной квитанцией для вызова разрешения конфликта
    const applied = account.applyTransaction(tx2, invalidReceipt2);
    expect(applied).toBe(false); // Должно быть false из-за невалидной квитанции

    const state = account.getState();
    // Балансы должны откатиться к состоянию после tx1, а не отражать tx2
    expect(state.balanceA).toBe(initialBalanceA - tx1.amount);
    expect(state.balanceB).toBe(initialBalanceB + tx1.amount);
    expect(state.lastReceipt).toEqual(receipt1); // Последняя квитанция должна остаться receipt1
  });

  it('должен гарантировать, что JSON.stringify транзакции соответствует формату подписываемого сообщения', async () => {
    const tx: Transaction = {
      id: 'tx_json_test',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 100n,
      asset: 'ETH',
      nonce: 7,
    };

    const messageToSign = stringify(deepConvertBigIntToString(tx));
    const messageHashFromTx = EthCrypto.hash.keccak256(messageToSign);

    // Подписываем сообщение
    const senderSignature = await signMessage(entityAPrivateKey, tx);
    const receiverSignature = await signMessage(entityBPrivateKey, tx);

    // Восстанавливаем публичные ключи, используя строку messageToSign
    const recoveredPublicKeySender = recoverPublicKey(messageToSign, senderSignature);
    const recoveredPublicKeyReceiver = recoverPublicKey(messageToSign, receiverSignature);

    // Убедимся, что восстановленные публичные ключи совпадают с исходными (без префикса '0x' для сравнения)
    // entityAId и entityBId уже очищены (без '0x')
    expect(recoveredPublicKeySender.startsWith('0x') ? recoveredPublicKeySender.substring(2) : recoveredPublicKeySender).toBe(entityAId);
    expect(recoveredPublicKeyReceiver.startsWith('0x') ? recoveredPublicKeyReceiver.substring(2) : recoveredPublicKeyReceiver).toBe(entityBId);

    // Дополнительно проверяем, что хеш строкового представления сообщения консистентен
    const expectedMessageHash = EthCrypto.hash.keccak256(stringify(deepConvertBigIntToString(tx)));
    expect(messageHashFromTx).toBe(expectedMessageHash);
  });
});
