import { Level } from 'level';
import { RLP } from '@ethereumjs/rlp';
import { Entity } from './entity';
import { EntityID, Input, Block, EntityState } from './types';
import { WebSocketServer, WebSocket } from 'ws';

// Helper function to serialize data for RLP encoding
function serializeForRLP(obj: any): any {
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
  if (obj instanceof Buffer) {
    return new Uint8Array(obj);
  }
  if (obj instanceof EntityState) {
    return serializeForRLP(obj.toJSON());
  }
  return obj;
}

export class Server {
  private db: Level<string, Uint8Array>;
  private entities: Map<EntityID, Entity>;
  private mempool: Map<EntityID, Input[]>;
  private currentBlockHeight: number;
  private wss: WebSocketServer;
  private blockProcessor: NodeJS.Timeout | null = null;

  constructor(dbPath: string, wsPort: number = 8080) {
    this.db = new Level<string, Uint8Array>(dbPath, { valueEncoding: 'view' });
    this.entities = new Map();
    this.mempool = new Map();
    this.currentBlockHeight = 0;
    this.wss = new WebSocketServer({ port: wsPort });

    this.wss.on('connection', ws => {
      console.log('Client connected');
      ws.on('close', () => console.log('Client disconnected'));
    });
  }

  public async start(): Promise<void> {
    await this.db.open();
    await this.restoreState();
    this.blockProcessor = setInterval(() => this.processBlock(), 100); // Изменено на 100мс
  }

  public async stop(): Promise<void> {
    if (this.blockProcessor) {
      clearInterval(this.blockProcessor);
    }
    await new Promise<void>((resolve) => this.wss.close(() => resolve()));
    await this.db.close();
  }

  public addEntity(entity: Entity): void {
    this.entities.set(entity.getState().id, entity);
  }

  public getEntity(id: EntityID): Entity | undefined {
    return this.entities.get(id);
  }

  public submitInput(entityId: EntityID, input: Input): void {
    if (!this.mempool.has(entityId)) {
      this.mempool.set(entityId, []);
    }
    this.mempool.get(entityId)!.push(input);
  }

  private async processBlock(): Promise<void> {
    const blockInputs: [Input[], any][] = [];
    for (const [entityId, inputs] of this.mempool.entries()) {
      const entity = this.entities.get(entityId);
      if (entity) {
        // Согласно ТЗ: inputs = [[someinputdata, entitystate]]
        // someinputdata здесь - это транзакции
        blockInputs.push([inputs, entity.getState().toJSON()]);
      }
    }

    if (blockInputs.length === 0) {
      return;
    }

    const block: Block = {
      height: this.currentBlockHeight,
      timestamp: Date.now(),
      inputs: blockInputs,
    };

    const rlpEncodedBlock = RLP.encode(serializeForRLP(block));
    await this.db.put(`block_${this.currentBlockHeight}`, rlpEncodedBlock);

    // For WebSocket broadcast, use JSON.stringify with a custom replacer
    // to handle BigInt and Map, as WebSocket clients expect JSON.
    this.broadcast(JSON.stringify(block, (key, value) => {
      if (typeof value === 'bigint') {
        return value.toString() + 'n'; // Append 'n' to BigInt strings for client-side parsing
      }
      if (value instanceof Map) {
        return Array.from(value.entries()); // Convert Map to array of entries for JSON
      }
      if (value instanceof Buffer) {
        return { type: 'Buffer', data: Array.from(value) }; // Serialize Buffer to a recognizable object
      }
      return value;
    }));

    console.log(`Block ${this.currentBlockHeight} created and saved.`);
    this.currentBlockHeight++;
    this.mempool.clear();
  }

  private broadcast(data: string): void {
    this.wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(data);
      }
    });
  }

  private async restoreState(): Promise<void> {
    try {
      const latestBlockHeight = await this.findLatestBlockHeight();
      if (latestBlockHeight >= 0) {
        this.currentBlockHeight = latestBlockHeight + 1;
        console.log(`Restored state from block ${latestBlockHeight}. Next block will be ${this.currentBlockHeight}.`);
      } else {
        console.log('No previous state found, starting from genesis.');
      }
    } catch (error) {
      console.error('Failed to restore state:', error);
    }
  }

  private async findLatestBlockHeight(): Promise<number> {
    let height = -1;
    for await (const key of this.db.keys({ reverse: true, limit: 1 })) {
        if (key.startsWith('block_')) {
            height = parseInt(key.split('_')[1], 10);
            break;
        }
    }
    return height;
  }
}
