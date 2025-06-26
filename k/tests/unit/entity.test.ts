import { Entity } from '../../src/entity';
import * as EthCrypto from 'eth-crypto';

describe('Сущность (Entity)', () => {
  it('должна создавать сущность с валидным состоянием', () => {
    const identity = EthCrypto.createIdentity();
    const entity = new Entity(identity);
    const state = entity.getState();

    expect(state.id).toBeDefined();
    expect(state.reserves).toBeInstanceOf(Map);
    expect(state.debts).toBeInstanceOf(Map);
    expect(state.accounts).toBeInstanceOf(Map);
    expect(state.quorumMembers).toBeDefined();
  });

  it('должна создавать счет с другой сущностью', () => {
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
