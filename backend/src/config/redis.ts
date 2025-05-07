import Redis from 'ioredis';
import { RedisOptions } from 'ioredis';

interface RedisNode {
  host: string;
  port: number;
}

interface RedisConfig {
  nodes: RedisNode[];
  options?: RedisOptions;
}

class RedisCluster {
  private static instance: Redis.Cluster | null = null;
  private static nodes: RedisNode[] = [
    { host: process.env.REDIS_HOST_1 || 'localhost', port: parseInt(process.env.REDIS_PORT_1 || '6379') },
    { host: process.env.REDIS_HOST_2 || 'localhost', port: parseInt(process.env.REDIS_PORT_2 || '6380') },
    { host: process.env.REDIS_HOST_3 || 'localhost', port: parseInt(process.env.REDIS_PORT_3 || '6381') }
  ];

  private static defaultOptions: RedisOptions = {
    scaleReads: 'slave',
    maxRedirections: 16,
    retryDelayOnFailover: 100,
    retryDelayOnClusterDown: 100,
    retryDelayOnTryAgain: 100,
    clusterRetryStrategy: (times: number) => {
      const delay = Math.min(100 + Math.random() * 1000, 2000);
      console.log(`Cluster connection attempt ${times}, retrying in ${delay}ms`);
      return delay;
    }
  };

  static async getConnection(config?: RedisConfig): Promise<Redis.Cluster> {
    if (this.instance) {
      return this.instance;
    }

    const nodes = config?.nodes || this.nodes;
    const options = {
      ...this.defaultOptions,
      ...config?.options
    };

    try {
      this.instance = new Redis.Cluster(nodes, options);

      this.instance.on('connect', () => {
        console.log('Connected to Redis cluster');
      });

      this.instance.on('error', (error) => {
        console.error('Redis cluster error:', error);
      });

      this.instance.on('node:added', (node) => {
        console.log('Node added to Redis cluster:', node);
      });

      this.instance.on('node:removed', (node) => {
        console.log('Node removed from Redis cluster:', node);
      });

      // Test connection
      await this.instance.ping();
      return this.instance;
    } catch (error) {
      console.error('Failed to create Redis cluster:', error);
      throw error;
    }
  }

  static async closeConnection(): Promise<void> {
    if (this.instance) {
      await this.instance.quit();
      this.instance = null;
    }
  }
}

// Helper functions for common Redis operations with retry logic
export class RedisService {
  private static readonly MAX_RETRIES = 3;
  private static readonly RETRY_DELAY = 1000;

  static async get(key: string): Promise<string | null> {
    return this.withRetry(async (client) => {
      return client.get(key);
    });
  }

  static async set(key: string, value: string, ttl?: number): Promise<'OK'> {
    return this.withRetry(async (client) => {
      if (ttl) {
        return client.set(key, value, 'EX', ttl);
      }
      return client.set(key, value);
    });
  }

  static async del(key: string): Promise<number> {
    return this.withRetry(async (client) => {
      return client.del(key);
    });
  }

  static async hget(key: string, field: string): Promise<string | null> {
    return this.withRetry(async (client) => {
      return client.hget(key, field);
    });
  }

  static async hset(key: string, field: string, value: string): Promise<number> {
    return this.withRetry(async (client) => {
      return client.hset(key, field, value);
    });
  }

  private static async withRetry<T>(
    operation: (client: Redis.Cluster) => Promise<T>,
    retries = this.MAX_RETRIES
  ): Promise<T> {
    try {
      const client = await RedisCluster.getConnection();
      return await operation(client);
    } catch (error) {
      if (retries > 0) {
        await new Promise(resolve => setTimeout(resolve, this.RETRY_DELAY));
        return this.withRetry(operation, retries - 1);
      }
      throw error;
    }
  }
}

export { RedisCluster, RedisConfig, RedisNode }; 