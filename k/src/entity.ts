// k/src/entity.ts
import { EntityID, EntityState, Transaction, Receipt, Proposal, Signature, AccountState } from './types';
import { Account } from './account';
import { signMessage, recoverPublicKey, hashMessage, removeHexPrefix } from './crypto';
import * as EthCrypto from 'eth-crypto';
import stringify from 'fast-json-stable-stringify';

// Helper function to deep convert BigInt to string (duplicate from crypto.ts for consistency)
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

interface EthCryptoIdentity {
  privateKey: string;
  publicKey: string;
  address: string;
}

export class Entity {
  private state: EntityState;
  private identity: EthCryptoIdentity; // Use custom interface

  constructor(identity: EthCryptoIdentity, quorumMembers: EntityID[] = []) {
    this.identity = identity;
    this.state = {
      id: removeHexPrefix(identity.publicKey), // Ensure EntityID is without '0x' prefix
      reserves: new Map(),
      debts: new Map(),
      accounts: new Map(),
      quorumMembers: quorumMembers.length > 0 ? quorumMembers.map(removeHexPrefix) : [removeHexPrefix(identity.publicKey)], // Clean quorum members
    };
  }

  public getState(): EntityState {
    return this.state;
  }

  public getIdentity(): EthCryptoIdentity {
    return this.identity;
  }

  /**
   * Creates a new account (channel) with another entity.
   * @param peerId The public key of the peer entity.
   */
  public createAccount(peerId: EntityID): Account {
    const cleanPeerId = removeHexPrefix(peerId);
    const cleanMyId = removeHexPrefix(this.state.id);
    const account = new Account(cleanMyId, cleanPeerId);
    this.state.accounts.set(cleanPeerId, account.getState());
    return account;
  }

  /**
   * Gets an existing account by peer ID.
   * @param peerId The public key of the peer entity.
   * @returns The Account instance, or undefined if not found.
   */
  public getAccount(peerId: EntityID): Account | undefined {
    const cleanPeerId = removeHexPrefix(peerId);
    const accountState = this.state.accounts.get(cleanPeerId);
    if (!accountState) return undefined;
    // Reconstruct Account object from state
    const account = new Account(this.getPartyAFromChannelId(accountState.channelId), this.getPartyBFromChannelId(accountState.channelId));
    // Manually set the internal state (this is a simplified approach for simulation)
    (account as any).state = accountState; 
    return account;
  }

  /**
   * Initiates a transaction within an existing account.
   * This entity signs the transaction. The receiver will also need to sign for a valid receipt.
   * @param receiverId The public key of the receiving entity.
   * @param amount The amount to send (BigInt).
   * @param asset The asset type (e.g., "USD").
   * @returns The signed transaction and a partial receipt.
   */
  public async initiateTransaction(
    receiverId: EntityID,
    amount: bigint,
    asset: string
  ): Promise<{ transaction: Transaction; partialReceipt: Receipt }> {
    const cleanReceiverId = removeHexPrefix(receiverId);
    if (!this.state.accounts.has(cleanReceiverId)) {
      throw new Error(`No account found with ${cleanReceiverId}. Create one first.`);
    }

    const transaction: Transaction = {
      id: hashMessage(stringify(deepConvertBigIntToString({ sender: this.state.id, receiver: cleanReceiverId, amount, asset, nonce: Date.now() }))), // Hash the stringified object
      senderId: this.state.id,
      receiverId: cleanReceiverId,
      amount: amount,
      asset: asset,
      nonce: Date.now(), // Simple nonce for uniqueness
    };

    // Sender signs the transaction
    const senderSignature = await signMessage(this.identity.privateKey, transaction);

    const partialReceipt: Receipt = {
      transactionId: transaction.id,
      signatures: [senderSignature],
      timestamp: Date.now(),
    };

    return { transaction, partialReceipt };
  }

  /**
   * Processes an incoming transaction and signs it if valid.
   * @param transaction The incoming transaction.
   * @param senderSignature The signature from the sender.
   * @returns A full receipt if signed, or null if invalid.
   */
  public async processIncomingTransaction(transaction: Transaction, senderSignature: Signature): Promise<Receipt | null> {
    // 1. Verify sender's signature
    const recoveredSenderPublicKey = removeHexPrefix(recoverPublicKey(stringify(deepConvertBigIntToString(transaction)), senderSignature));
    const cleanTransactionSenderId = removeHexPrefix(transaction.senderId);

    if (recoveredSenderPublicKey !== cleanTransactionSenderId) {
      console.error(`Invalid sender signature for transaction ${transaction.id}`);
      return null;
    }

    // 2. Check if account exists and is valid
    const account = this.getAccount(cleanTransactionSenderId); // Sender is the peer for this entity
    if (!account) {
      console.error(`No account found for incoming transaction from ${cleanTransactionSenderId}`);
      return null;
    }

    // 3. Check if this entity is the receiver
    if (removeHexPrefix(transaction.receiverId) !== this.state.id) {
      console.error(`This entity is not the receiver of transaction ${transaction.id}`);
      return null;
    }

    // 4. Perform any additional validation (e.g., sufficient balance in reserves, etc.)
    // For simplicity, we assume reserves are managed separately or implicitly.
    // In a real system, this would involve checking if the entity has enough funds to receive.

    // 5. Receiver signs the transaction
    const receiverSignature = await signMessage(this.identity.privateKey, transaction);

    const fullReceipt: Receipt = {
      transactionId: transaction.id,
      signatures: [senderSignature, receiverSignature],
      timestamp: Date.now(),
    };

    // Update account state with the new receipt
    account.applyTransaction(transaction, fullReceipt);
    this.state.accounts.set(cleanTransactionSenderId, account.getState()); // Update the stored state

    return fullReceipt;
  }

  /**
   * Processes a full receipt (signed by both parties) and applies it to the account.
   * This is typically called by the sender after receiving the receiver's signature.
   * @param transaction The original transaction.
   * @param fullReceipt The receipt signed by both parties.
   * @returns True if the receipt was applied, false otherwise.
   */
  public applyFullReceipt(transaction: Transaction, fullReceipt: Receipt): boolean {
    const peerId = removeHexPrefix(transaction.receiverId) === this.state.id ? removeHexPrefix(transaction.senderId) : removeHexPrefix(transaction.receiverId);
    const account = this.getAccount(peerId);
    if (!account) {
      console.error(`Account not found for transaction ${transaction.id} when applying full receipt.`);
      return false;
    }

    const applied = account.applyTransaction(transaction, fullReceipt);
    if (applied) {
      this.state.accounts.set(peerId, account.getState()); // Update the stored state
    }
    return applied;
  }

  /**
   * Votes on a proposal.
   * @param proposal The proposal to vote on.
   * @param signature The signature of the quorum member.
   * @returns True if the vote is valid and counted, false otherwise.
   */
  public voteProposal(proposal: Proposal, signature: Signature): boolean {
    const cleanIdentityPublicKey = removeHexPrefix(this.identity.publicKey);
    if (!this.state.quorumMembers.includes(cleanIdentityPublicKey)) {
      console.warn(`Entity ${this.state.id} is not a quorum member and cannot vote.`);
      return false;
    }

    const recoveredPublicKey = removeHexPrefix(recoverPublicKey(stringify(deepConvertBigIntToString(proposal)), signature));
    if (!this.state.quorumMembers.includes(recoveredPublicKey)) {
      console.warn(`Signature from non-quorum member ${recoveredPublicKey} for proposal ${proposal.id}.`);
      return false;
    }

    // In a real system, you'd add the signature to the proposal and check if quorum is met.
    // For this simulation, we'll just check if the signature is from a valid quorum member.
    console.log(`Entity ${this.state.id} voted on proposal ${proposal.id}.`);
    return true;
  }

  /**
   * Checks if a proposal has met its quorum.
   * @param proposal The proposal to check.
   * @returns True if quorum is met, false otherwise.
   */
  public checkQuorum(proposal: Proposal): boolean {
    const validSignatures = new Set<EntityID>();
    for (const sig of proposal.signatures) {
      try {
        const recovered = removeHexPrefix(recoverPublicKey(stringify(deepConvertBigIntToString(proposal)), sig));
        if (this.state.quorumMembers.includes(recovered)) {
          validSignatures.add(recovered);
        }
      } catch (e) {
        console.warn(`Invalid signature in proposal ${proposal.id}: ${e}`);
      }
    }
    // Example: 3-of-5 quorum. This needs to be dynamic based on quorumMembers.length
    // For simplicity, let's say it's 60% of quorum members.
    const requiredSignatures = Math.ceil(this.state.quorumMembers.length * 0.6);
    return validSignatures.size >= requiredSignatures;
  }

  // Helper to extract party A from channelId
  private getPartyAFromChannelId(channelId: string): EntityID {
    return channelId.split('-')[0];
  }

  // Helper to extract party B from channelId
  private getPartyBFromChannelId(channelId: string): EntityID {
    return channelId.split('-')[1];
  }
}
