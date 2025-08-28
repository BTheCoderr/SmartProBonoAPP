const crypto = require('crypto');
const { createLogger } = require('./logger');

const logger = createLogger('encryption');

class Encryption {
  constructor() {
    this.algorithm = 'aes-256-gcm';
    this.keyLength = 32; // 256 bits
    this.ivLength = 16; // 128 bits
    this.saltLength = 64;
    this.tagLength = 16;
    
    // Ensure encryption key is set
    if (!process.env.ENCRYPTION_KEY) {
      logger.error('ENCRYPTION_KEY environment variable is not set');
      throw new Error('Encryption key is required');
    }
  }

  // Generate a secure key from password and salt
  async generateKey(password, salt) {
    return new Promise((resolve, reject) => {
      crypto.pbkdf2(
        password,
        salt,
        100000, // Number of iterations
        this.keyLength,
        'sha512',
        (err, key) => {
          if (err) reject(err);
          resolve(key);
        }
      );
    });
  }

  // Encrypt sensitive data
  async encrypt(data) {
    try {
      // Generate a random salt and IV
      const salt = crypto.randomBytes(this.saltLength);
      const iv = crypto.randomBytes(this.ivLength);

      // Generate encryption key
      const key = await this.generateKey(process.env.ENCRYPTION_KEY, salt);

      // Create cipher
      const cipher = crypto.createCipheriv(this.algorithm, key, iv);

      // Encrypt the data
      let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
      encrypted += cipher.final('hex');

      // Get the auth tag
      const tag = cipher.getAuthTag();

      // Combine all components for storage
      const result = {
        encrypted: encrypted,
        iv: iv.toString('hex'),
        salt: salt.toString('hex'),
        tag: tag.toString('hex')
      };

      logger.info('Data encrypted successfully');
      return result;
    } catch (error) {
      logger.error('Encryption failed:', error);
      throw new Error('Encryption failed');
    }
  }

  // Decrypt sensitive data
  async decrypt(encryptedData) {
    try {
      // Convert hex strings back to buffers
      const iv = Buffer.from(encryptedData.iv, 'hex');
      const salt = Buffer.from(encryptedData.salt, 'hex');
      const tag = Buffer.from(encryptedData.tag, 'hex');
      const encrypted = encryptedData.encrypted;

      // Generate the same key using the stored salt
      const key = await this.generateKey(process.env.ENCRYPTION_KEY, salt);

      // Create decipher
      const decipher = crypto.createDecipheriv(this.algorithm, key, iv);
      decipher.setAuthTag(tag);

      // Decrypt the data
      let decrypted = decipher.update(encrypted, 'hex', 'utf8');
      decrypted += decipher.final('utf8');

      logger.info('Data decrypted successfully');
      return JSON.parse(decrypted);
    } catch (error) {
      logger.error('Decryption failed:', error);
      throw new Error('Decryption failed');
    }
  }

  // Encrypt specific fields in an object
  async encryptFields(data, sensitiveFields) {
    const result = { ...data };
    
    for (const field of sensitiveFields) {
      if (result[field]) {
        const encrypted = await this.encrypt(result[field]);
        result[field] = {
          isEncrypted: true,
          data: encrypted
        };
      }
    }
    
    return result;
  }

  // Decrypt specific fields in an object
  async decryptFields(data, sensitiveFields) {
    const result = { ...data };
    
    for (const field of sensitiveFields) {
      if (result[field] && result[field].isEncrypted) {
        result[field] = await this.decrypt(result[field].data);
      }
    }
    
    return result;
  }

  // Hash sensitive identifiers (like SSN)
  hashIdentifier(identifier) {
    return crypto
      .createHash('sha256')
      .update(identifier + process.env.ENCRYPTION_KEY)
      .digest('hex');
  }

  // Generate a secure random token
  generateToken(length = 32) {
    return crypto.randomBytes(length).toString('hex');
  }
}

// Export singleton instance
module.exports = new Encryption(); 