// k/src/types.ts

export type EntityID = string; // Public key of the entity (hex string, with 0x prefix)
export type Signature = string; // Hex string of the signature

export interface Input {
  type: 'transaction' | 'proposal';
  data: any;
}

export interface Transaction {
  id: string; // Unique transaction ID
  senderId: EntityID;
  receiverId: EntityID;
  amount: bigint;
  asset: string; // e.g., "USD", "BTC"
  nonce: number; // To prevent replay attacks
}

export interface Receipt {
  transactionId: string;
  signatures: Signature[]; // Signatures from both sender and receiver
  timestamp: number;
  transaction: Transaction; // Add the full transaction object to the receipt
}

export interface Proposal {
  id: string;
  entityId: EntityID;
  type: 'transfer' | 'account_open' | 'quorum_change';
  data: any; // Specific data for the proposal type
  signatures: Signature[]; // Signatures from quorum members
}

export interface AccountState {
  channelId: string;
  balanceA: bigint; // Balance for Entity A
  balanceB: bigint; // Balance for Entity B
  lastReceipt: Receipt | null;
}

export class EntityState {
  id: EntityID;
  reserves: Map<string, bigint>; // asset -> amount
  debts: Map<string, bigint>; // asset -> amount
  accounts: Map<EntityID, AccountState>; // peerId -> AccountState
  quorumMembers: EntityID[]; // Public keys of quorum members

  constructor(id: EntityID, quorumMembers: EntityID[]) {
    this.id = id;
    this.reserves = new Map();
    this.debts = new Map();
    this.accounts = new Map();
    this.quorumMembers = quorumMembers;
  }

  toJSON() {
    return {
      id: this.id,
      reserves: Array.from(this.reserves.entries()),
      debts: Array.from(this.debts.entries()),
      accounts: Array.from(this.accounts.entries()),
      quorumMembers: this.quorumMembers,
    };
  }
}

export type EntityMap = Map<EntityID, EntityState>;

export interface Block {
  height: number;
  timestamp: number;
  inputs: any[];
}
