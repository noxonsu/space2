// k/src/types.ts

export type EntityID = string; // Public key of the entity (hex string, with 0x prefix)
export type Signature = string; // Hex string of the signature

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

export interface EntityState {
  id: EntityID;
  reserves: Map<string, bigint>; // asset -> amount
  debts: Map<string, bigint>; // asset -> amount
  accounts: Map<EntityID, AccountState>; // peerId -> AccountState
  quorumMembers: EntityID[]; // Public keys of quorum members
}

export type EntityMap = Map<EntityID, EntityState>;

export interface Block {
  height: number;
  timestamp: number;
  transactions: Transaction[]; // Transactions included in this block
  stateRoot: string; // Merkle root of the EntityMap state (future)
}
