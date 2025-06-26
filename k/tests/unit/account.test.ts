// k/tests/unit/account.test.ts
import { Account } from '../../src/account';
import { Transaction, Receipt, EntityID } from '../../src/types';
import { signMessage, recoverPublicKey } from '../../src/crypto';
import * as EthCrypto from 'eth-crypto';
import stringify from 'fast-json-stable-stringify'; // Добавляем импорт stringify

// Helper function to deep convert BigInt to string (duplicate from crypto.ts for testing purposes)
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
    // Ensure public keys are uncompressed and without '0x' prefix
    entityAId = identityA.publicKey.startsWith('0x') ? identityA.publicKey.substring(2) : identityA.publicKey;
    entityBId = identityB.publicKey.startsWith('0x') ? identityB.publicKey.substring(2) : identityB.publicKey;
    console.log(`Entity A ID: ${entityAId}`);
    console.log(`Entity B ID: ${entityBId}`);
  });

  it('should initialize with zero balances', () => {
    const account = new Account(entityAId, entityBId);
    const state = account.getState();
    expect(state.balanceA).toBe(0n);
    expect(state.balanceB).toBe(0n);
    expect(state.lastReceipt).toBeNull();
    expect(state.channelId).toBe([entityAId, entityBId].sort().join('-'));
  });

  it('should apply a valid transaction and update balances', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    // Manually set initial balances for testing purposes
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
    console.log('messageHashForSigning (tx1):', messageHashForSigning);

    const senderSignature = await signMessage(entityAPrivateKey, tx);
    const receiverSignature = await signMessage(entityBPrivateKey, tx);

    const receipt: Receipt = {
      transactionId: tx.id,
      signatures: [senderSignature, receiverSignature],
      timestamp: Date.now(),
      transaction: tx, // Add the transaction object
    };

    const applied = account.applyTransaction(tx, receipt);
    expect(applied).toBe(true);
    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA - tx.amount);
    expect(state.balanceB).toBe(initialBalanceB + tx.amount);
    expect(state.lastReceipt).toEqual(receipt);
  });

  it('should reject a transaction with invalid sender signature', async () => {
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
    console.log('messageHashForSigning (tx2):', messageHashForSigning2);

    // Invalid signature (e.g., from a random private key)
    const invalidSignature = await signMessage('0x1234567890123456789012345678901234567890123456789012345678901234', tx);
    const receiverSignature = await signMessage(entityBPrivateKey, tx);

    const receipt: Receipt = {
      transactionId: tx.id,
      signatures: [invalidSignature, receiverSignature],
      timestamp: Date.now(),
      transaction: tx, // Add the transaction object
    };

    const applied = account.applyTransaction(tx, receipt);
    expect(applied).toBe(false); // Should be false due to invalid signature
    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA); // Balances should not change
    expect(state.balanceB).toBe(initialBalanceB);
    expect(state.lastReceipt).toBeNull(); // Last receipt should not be updated
  });

  it('should reject a transaction with missing receiver signature', async () => {
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
    console.log('messageHashForSigning (tx3):', messageHashForSigning3);

    const senderSignature = await signMessage(entityAPrivateKey, tx);

    const receipt: Receipt = {
      transactionId: tx.id,
      signatures: [senderSignature], // Missing receiver signature
      timestamp: Date.now(),
      transaction: tx, // Add the transaction object
    };

    const applied = account.applyTransaction(tx, receipt);
    expect(applied).toBe(false);
    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA);
    expect(state.balanceB).toBe(initialBalanceB);
    expect(state.lastReceipt).toBeNull();
  });

  it('should handle conflict resolution by "right wins" rule (no change if no last receipt)', async () => {
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

    // Simulate a conflict without a valid last receipt
    account.resolveConflict(tx);

    const state = account.getState();
    expect(state.balanceA).toBe(initialBalanceA); // Should remain unchanged
    expect(state.balanceB).toBe(initialBalanceB);
  });

  it('should handle conflict resolution by "right wins" rule (revert to last receipt state)', async () => {
    const account = new Account(entityAId, entityBId);
    const initialBalanceA = 100n;
    const initialBalanceB = 50n;
    (account as any).state.balanceA = initialBalanceA;
    (account as any).state.balanceB = initialBalanceB;

    // First, apply a valid transaction to set a lastReceipt
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
    console.log('messageHashForSigning (tx5):', messageHashForSigning5);

    const senderSignature1 = await signMessage(entityAPrivateKey, tx1);
    const receiverSignature1 = await signMessage(entityBPrivateKey, tx1);
    const receipt1: Receipt = {
      transactionId: tx1.id,
      signatures: [senderSignature1, receiverSignature1],
      timestamp: Date.now(),
      transaction: tx1, // Add the transaction object
    };
    account.applyTransaction(tx1, receipt1);

    // Now, simulate a conflicting transaction that would be invalid
    const tx2: Transaction = {
      id: 'tx6',
      senderId: entityAId,
      receiverId: entityBId,
      amount: 50n, // Large amount to make it obvious if applied
      asset: 'USD',
      nonce: 6,
    };
    // No valid receipt for tx2, or an invalid one
    const invalidReceipt2: Receipt = {
      transactionId: tx2.id,
      signatures: [], // Invalid signatures
      timestamp: Date.now(),
      transaction: tx2, // Add the transaction object
    };

    // Directly call applyTransaction with invalid receipt to trigger conflict resolution
    const applied = account.applyTransaction(tx2, invalidReceipt2);
    expect(applied).toBe(false); // Should be false due to invalid receipt

    const state = account.getState();
    // Balances should revert to the state after tx1, not reflect tx2
    expect(state.balanceA).toBe(initialBalanceA - tx1.amount);
    expect(state.balanceB).toBe(initialBalanceB + tx1.amount);
    expect(state.lastReceipt).toEqual(receipt1); // Last receipt should still be receipt1
  });

  it('should ensure JSON.stringify of transaction matches the signed message format', async () => {
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

    // Sign the message
    const senderSignature = await signMessage(entityAPrivateKey, tx);
    const receiverSignature = await signMessage(entityBPrivateKey, tx);

    // Recover public keys using the messageToSign string
    const recoveredPublicKeySender = recoverPublicKey(messageToSign, senderSignature);
    const recoveredPublicKeyReceiver = recoverPublicKey(messageToSign, receiverSignature);

    // Ensure recovered public keys match the original public keys (without '0x' prefix for comparison)
    // entityAId and entityBId are already clean (without '0x')
    expect(recoveredPublicKeySender.startsWith('0x') ? recoveredPublicKeySender.substring(2) : recoveredPublicKeySender).toBe(entityAId);
    expect(recoveredPublicKeyReceiver.startsWith('0x') ? recoveredPublicKeyReceiver.substring(2) : recoveredPublicKeyReceiver).toBe(entityBId);

    // Additionally, verify that the hash of the stringified message is consistent
    const expectedMessageHash = EthCrypto.hash.keccak256(stringify(deepConvertBigIntToString(tx)));
    expect(messageHashFromTx).toBe(expectedMessageHash);
  });
});
