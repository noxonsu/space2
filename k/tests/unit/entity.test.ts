import { Entity } from '../../src/entity';
import * as EthCrypto from 'eth-crypto';

describe('Entity', () => {
  it('should create an entity with a valid state', () => {
    const identity = EthCrypto.createIdentity();
    const entity = new Entity(identity);
    const state = entity.getState();

    expect(state.id).toBeDefined();
    expect(state.reserves).toBeInstanceOf(Map);
    expect(state.debts).toBeInstanceOf(Map);
    expect(state.accounts).toBeInstanceOf(Map);
    expect(state.quorumMembers).toBeDefined();
  });

  it('should create an account with another entity', () => {
    const entityAIdentity = EthCrypto.createIdentity();
    const entityBIdentity = EthCrypto.createIdentity();
    const entityA = new Entity(entityAIdentity);

    const account = entityA.createAccount(entityBIdentity.publicKey);
    expect(account).toBeDefined();

    const entityAState = entityA.getState();
    const cleanPeerId = entityBIdentity.publicKey.startsWith('0x') ? entityBIdentity.publicKey.slice(2) : entityBIdentity.publicKey;
    expect(entityAState.accounts.has(cleanPeerId)).toBe(true);
  });
});
