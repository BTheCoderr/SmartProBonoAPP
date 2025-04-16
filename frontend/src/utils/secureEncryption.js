/**
 * secureEncryption.js
 * Utility for client-side encryption of sensitive data
 * Uses the Web Crypto API for strong encryption
 */

/**
 * Generates a new encryption key
 * @returns {Promise<CryptoKey>} The generated encryption key
 */
export const generateEncryptionKey = async () => {
  return window.crypto.subtle.generateKey(
    {
      name: 'AES-GCM',
      length: 256,
    },
    true, // extractable
    ['encrypt', 'decrypt']
  );
};

/**
 * Exports a CryptoKey to raw format for storage
 * @param {CryptoKey} key - The key to export
 * @returns {Promise<string>} Base64 encoded key
 */
export const exportKey = async key => {
  const exported = await window.crypto.subtle.exportKey('raw', key);
  return bufferToBase64(exported);
};

/**
 * Imports a key from base64 string
 * @param {string} keyStr - Base64 encoded key
 * @returns {Promise<CryptoKey>} The imported key
 */
export const importKey = async keyStr => {
  const keyData = base64ToBuffer(keyStr);
  return window.crypto.subtle.importKey(
    'raw',
    keyData,
    {
      name: 'AES-GCM',
      length: 256,
    },
    true,
    ['encrypt', 'decrypt']
  );
};

/**
 * Encrypts data using AES-GCM
 * @param {CryptoKey} key - The encryption key
 * @param {string} data - The data to encrypt
 * @returns {Promise<{ciphertext: string, iv: string}>} Encrypted data and IV
 */
export const encryptData = async (key, data) => {
  // Create an initialization vector
  const iv = window.crypto.getRandomValues(new Uint8Array(12));

  // Encode the data
  const encodedData = new TextEncoder().encode(data);

  // Encrypt the data
  const encryptedData = await window.crypto.subtle.encrypt(
    {
      name: 'AES-GCM',
      iv,
    },
    key,
    encodedData
  );

  return {
    ciphertext: bufferToBase64(encryptedData),
    iv: bufferToBase64(iv),
  };
};

/**
 * Decrypts data using AES-GCM
 * @param {CryptoKey} key - The decryption key
 * @param {string} ciphertext - The encrypted data (base64)
 * @param {string} iv - The initialization vector (base64)
 * @returns {Promise<string>} Decrypted data
 */
export const decryptData = async (key, ciphertext, iv) => {
  // Convert base64 strings to ArrayBuffers
  const encryptedData = base64ToBuffer(ciphertext);
  const ivBuffer = base64ToBuffer(iv);

  // Decrypt the data
  const decryptedData = await window.crypto.subtle.decrypt(
    {
      name: 'AES-GCM',
      iv: ivBuffer,
    },
    key,
    encryptedData
  );

  // Decode the data
  return new TextDecoder().decode(decryptedData);
};

/**
 * Creates a secure random token
 * @param {number} length - Length of token in bytes
 * @returns {string} Random token as hex string
 */
export const generateRandomToken = (length = 32) => {
  const buffer = new Uint8Array(length);
  window.crypto.getRandomValues(buffer);
  return Array.from(buffer)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
};

/**
 * Encrypts an entire message object for secure chat
 * @param {CryptoKey} key - The encryption key
 * @param {Object} message - The message object to encrypt
 * @returns {Promise<Object>} Encrypted message object
 */
export const encryptMessage = async (key, message) => {
  const messageStr = JSON.stringify(message);
  const { ciphertext, iv } = await encryptData(key, messageStr);

  return {
    encryptedContent: ciphertext,
    iv,
    timestamp: message.timestamp || new Date().toISOString(),
    senderId: message.senderId,
    // Include message type but not content
    type: message.type,
    encryptionVersion: '1.0',
  };
};

/**
 * Decrypts a message object from secure chat
 * @param {CryptoKey} key - The decryption key
 * @param {Object} encryptedMessage - The encrypted message object
 * @returns {Promise<Object>} Decrypted message object
 */
export const decryptMessage = async (key, encryptedMessage) => {
  const { encryptedContent, iv, timestamp, senderId, type } = encryptedMessage;

  const decryptedStr = await decryptData(key, encryptedContent, iv);
  const decryptedMessage = JSON.parse(decryptedStr);

  return {
    ...decryptedMessage,
    timestamp: timestamp || decryptedMessage.timestamp,
    senderId: senderId || decryptedMessage.senderId,
    type: type || decryptedMessage.type,
    decrypted: true,
  };
};

// Helper function to convert ArrayBuffer to Base64 string
const bufferToBase64 = buffer => {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
};

// Helper function to convert Base64 string to ArrayBuffer
const base64ToBuffer = base64 => {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
};

/**
 * Handles session key management for secure chat
 */
export const SessionKeyManager = {
  // Store encryption keys in memory for the session
  keys: new Map(),

  /**
   * Gets or generates a key for a specific chat session
   * @param {string} sessionId - The chat session ID
   * @returns {Promise<CryptoKey>} The session encryption key
   */
  async getSessionKey(sessionId) {
    if (this.keys.has(sessionId)) {
      return this.keys.get(sessionId);
    }

    // Check if we have a stored key in localStorage
    const storedKeyStr = localStorage.getItem(`chat_key_${sessionId}`);
    if (storedKeyStr) {
      try {
        const key = await importKey(storedKeyStr);
        this.keys.set(sessionId, key);
        return key;
      } catch (error) {
        console.error('Failed to import stored key:', error);
        // Fall through to generate a new key
      }
    }

    // Generate a new key
    const key = await generateEncryptionKey();
    this.keys.set(sessionId, key);

    // Store in localStorage (encrypted with a master key in a real app)
    const keyStr = await exportKey(key);
    localStorage.setItem(`chat_key_${sessionId}`, keyStr);

    return key;
  },

  /**
   * Securely saves a session key
   * @param {string} sessionId - The chat session ID
   * @param {CryptoKey} key - The key to save
   */
  async saveSessionKey(sessionId, key) {
    this.keys.set(sessionId, key);
    const keyStr = await exportKey(key);
    localStorage.setItem(`chat_key_${sessionId}`, keyStr);
  },

  /**
   * Clears a session key
   * @param {string} sessionId - The chat session ID to clear
   */
  clearSessionKey(sessionId) {
    this.keys.delete(sessionId);
    localStorage.removeItem(`chat_key_${sessionId}`);
  },
};

export default {
  generateEncryptionKey,
  exportKey,
  importKey,
  encryptData,
  decryptData,
  encryptMessage,
  decryptMessage,
  generateRandomToken,
  SessionKeyManager,
};
