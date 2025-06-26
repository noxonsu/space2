// k/src/crypto.ts
import * as EthCrypto from 'eth-crypto';
import stringify from 'fast-json-stable-stringify';
import { Transaction, Signature } from './types';

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

// New helper function to remove '0x' prefix
export function removeHexPrefix(hexString: string): string {
  return hexString.startsWith('0x') ? hexString.substring(2) : hexString;
}

export function hashMessage(message: string): string {
  return EthCrypto.hash.keccak256(message);
}

export async function signMessage(privateKey: string, tx: Transaction): Promise<Signature> {
  const messageToSign = stringify(deepConvertBigIntToString(tx));
  const messageHash = hashMessage(messageToSign);
  const signature = EthCrypto.sign(privateKey, messageHash);
  return signature;
}

export function recoverPublicKey(message: string, signature: Signature): string {
  const messageHash = hashMessage(message);
  const signer = EthCrypto.recoverPublicKey(signature, messageHash);
  return signer;
}
