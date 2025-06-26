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
  private entityA: EntityID;
  private entityB: EntityID;

  constructor(entityA: EntityID, entityB: EntityID) {
    // Ensure entity IDs are consistent (without '0x' prefix)
    this.entityA = removeHexPrefix(entityA);
    this.entityB = removeHexPrefix(entityB);
    this.state = {
      channelId: [this.entityA, this.entityB].sort().join('-'), // Canonical channel ID
      balanceA: 0n, // Balance for entityA
      balanceB: 0n, // Balance for entityB
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

    const cleanSenderId = removeHexPrefix(tx.senderId);
    const cleanReceiverId = removeHexPrefix(tx.receiverId);

    // Verify that the transaction is between the two parties of this account
    if (!((cleanSenderId === this.entityA && cleanReceiverId === this.entityB) || (cleanSenderId === this.entityB && cleanReceiverId === this.entityA))) {
        console.error(`Transaction ${tx.id} parties do not match account parties.`);
        return false;
    }

    // Apply the transaction based on the original entity IDs
    if (cleanSenderId === this.entityA) {
        this.state.balanceA = this.state.balanceA - tx.amount;
        this.state.balanceB = this.state.balanceB + tx.amount;
    } else {
        this.state.balanceB = this.state.balanceB - tx.amount;
        this.state.balanceA = this.state.balanceA + tx.amount;
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
    const recoveredPublicKey1 = removeHexPrefix(recoverPublicKey(messageToSign, receipt.signatures[0]));
    const recoveredPublicKey2 = removeHexPrefix(recoverPublicKey(messageToSign, receipt.signatures[1]));

    const recoveredPublicKeys = new Set<EntityID>([recoveredPublicKey1, recoveredPublicKey2]);

    // Check if both parties of the account have signed
    const hasPartyASigned = recoveredPublicKeys.has(this.entityA);
    const hasPartyBSigned = recoveredPublicKeys.has(this.entityB);

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
    if (this.state.lastReceipt && this.state.lastReceipt.transaction) {
        const lastTx = this.state.lastReceipt.transaction;
        console.log(`Reverting to state defined by last receipt for transaction ${this.state.lastReceipt.transactionId}`);
        
        // We need to know the initial balances before the last valid transaction.
        // This is a simplification. A real implementation would need a more robust state snapshotting.
        // For the test case, we assume we can recalculate from the last state.
        // Let's find out who was the sender in the last valid transaction
        if (removeHexPrefix(lastTx.senderId) === this.entityA) {
            // If A was the sender, they got debited and B got credited. To revert, we do the opposite.
            this.state.balanceA = this.state.balanceA + lastTx.amount;
            this.state.balanceB = this.state.balanceB - lastTx.amount;
        } else {
            // If B was the sender, they got debited and A got credited.
            this.state.balanceB = this.state.balanceB + lastTx.amount;
            this.state.balanceA = this.state.balanceA - lastTx.amount;
        }
        // Now, re-apply the last valid transaction to restore the correct state.
        this.applyTransaction(lastTx, this.state.lastReceipt);

    } else {
        console.log('No last receipt found. Channel state remains as is or reverts to initial.');
    }
  }

}
