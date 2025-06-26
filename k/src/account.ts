// k/src/account.ts
import { AccountState, EntityID, Transaction, Receipt, Signature } from './types';
import { recoverPublicKey, hashMessage, removeHexPrefix } from './crypto';
import stringify from 'fast-json-stable-stringify';
import * as EthCrypto from 'eth-crypto'; // Добавляем импорт EthCrypto

// Helper function to deep convert BigInt to string
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

export class Account {
  private state: AccountState;

  constructor(entityA: EntityID, entityB: EntityID) {
    // Ensure entity IDs are consistent (without '0x' prefix)
    const cleanEntityA = removeHexPrefix(entityA);
    const cleanEntityB = removeHexPrefix(entityB);
    this.state = {
      channelId: [cleanEntityA, cleanEntityB].sort().join('-'), // channelId will now be without '0x' prefix
      balanceA: 0n, // Use BigInt for balances
      balanceB: 0n,
      lastReceipt: null,
    };
  }

  public getState(): AccountState {
    return this.state;
  }

  /**
   * Applies a transaction to the account state.
   * @param tx The transaction to apply.
   * @param receipt The receipt for the transaction, signed by both parties.
   * @returns True if the transaction was applied successfully, false otherwise.
   */
  public applyTransaction(tx: Transaction, receipt: Receipt): boolean {
    if (!this.validateReceipt(tx, receipt)) {
      console.warn(`Invalid receipt for transaction ${tx.id}. Resolving conflict.`);
      this.resolveConflict(tx);
      return false;
    }

    // Ensure the transaction is for this channel
    // Compare with prefixed public keys
    const partyA = this.getPartyA();
    const partyB = this.getPartyB();

    const cleanSenderId = removeHexPrefix(tx.senderId);
    const cleanReceiverId = removeHexPrefix(tx.receiverId);


    if (cleanSenderId !== partyA && cleanSenderId !== partyB) {
      console.error(`Transaction ${tx.id} is not for this channel.`);
      return false;
    }

    // Apply the transaction
    if (cleanSenderId === partyA) {
      this.state.balanceA -= tx.amount;
      this.state.balanceB += tx.amount;
    } else {
      this.state.balanceB -= tx.amount;
      this.state.balanceA += tx.amount;
    }

    this.state.lastReceipt = receipt;
    return true;
  }

  /**
   * Validates a receipt by checking signatures.
   * A valid receipt must have signatures from both parties involved in the channel.
   * @param tx The transaction associated with the receipt.
   * @param receipt The receipt to validate.
   * @returns True if the receipt is valid, false otherwise.
   */
  private validateReceipt(tx: Transaction, receipt: Receipt): boolean {
    if (receipt.transactionId !== tx.id) {
      console.error(`Receipt transaction ID mismatch: ${receipt.transactionId} !== ${tx.id}`);
      return false;
    }
    if (receipt.signatures.length !== 2) {
      console.error(`Receipt for transaction ${tx.id} must have 2 signatures.`);
      return false;
    }

    const messageToSign = stringify(deepConvertBigIntToString(tx)); // Both parties sign the transaction itself
    console.log('messageToSign in validateReceipt:', messageToSign);
    const messageHashInValidate = EthCrypto.hash.keccak256(messageToSign); // Хеш сообщения для валидации
    console.log('messageHashInValidate:', messageHashInValidate); // Логируем хеш
    const recoveredPublicKey1 = removeHexPrefix(recoverPublicKey(messageToSign, receipt.signatures[0])); // Remove '0x' prefix
    const recoveredPublicKey2 = removeHexPrefix(recoverPublicKey(messageToSign, receipt.signatures[1])); // Remove '0x' prefix

    const partyA = this.getPartyA();
    const partyB = this.getPartyB();

    console.log('recoveredPublicKey1:', recoveredPublicKey1);
    console.log('recoveredPublicKey2:', recoveredPublicKey2);
    console.log('partyA:', partyA);
    console.log('partyB:', partyB);

    const recoveredPublicKeys = new Set<EntityID>();
    recoveredPublicKeys.add(recoveredPublicKey1);
    recoveredPublicKeys.add(recoveredPublicKey2);

    console.log('recoveredPublicKey1 (clean):', recoveredPublicKey1);
    console.log('recoveredPublicKey2 (clean):', recoveredPublicKey2);

    // Check if both parties have signed
    // Also ensure that the recovered public keys match the actual sender and receiver of the transaction
    const hasPartyASigned = recoveredPublicKeys.has(partyA);
    const hasPartyBSigned = recoveredPublicKeys.has(partyB);

    console.log('hasPartyASigned:', hasPartyASigned);
    console.log('hasPartyBSigned:', hasPartyBSigned);

    if (!hasPartyASigned || !hasPartyBSigned) {
      console.error(`Receipt for transaction ${tx.id} is missing signatures from one or both parties.`);
      return false;
    }

    return true;
  }

  /**
   * Resolves a conflict using the "right wins" rule (last valid receipt determines state).
   * If there's no last receipt, it implies a fresh state or an unconfirmed transaction.
   * @param conflictingTx The transaction that caused the conflict (optional, for context).
   */
  public resolveConflict(conflictingTx?: Transaction) {
    console.log(`Conflict detected in channel ${this.state.channelId}. Applying "right wins" rule.`);
    if (this.state.lastReceipt) {
      // Re-apply the last confirmed state based on the last valid receipt
      // This assumes the lastReceipt itself contains enough info or refers to a known state.
      // For simplicity, we'll just log that we revert to the last known good state.
      console.log(`Reverting to state defined by last receipt for transaction ${this.state.lastReceipt.transactionId}`);
      // In a real system, you might re-process the transaction from lastReceipt or load a snapshot.
      // For this simulation, we assume the state is implicitly correct if the lastReceipt is valid.
    } else {
      console.log('No last receipt found. Channel state remains as is or reverts to initial.');
      // Potentially reset balances to 0n or initial state if no valid history.
      // this.state.balanceA = 0n;
      // this.state.balanceB = 0n;
    }
  }

  private getPartyA(): EntityID {
    return this.state.channelId.split('-')[0];
  }

  private getPartyB(): EntityID {
    return this.state.channelId.split('-')[1];
  }
}
