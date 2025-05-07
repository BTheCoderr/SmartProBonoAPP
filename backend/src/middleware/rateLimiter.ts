import Redis from 'ioredis';

interface RateLimiterOptions {
  windowMs: number;
  maxRequests: number;
  keyPrefix?: string;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  retryAfter?: number;
}

export class RateLimiter {
  private redis: Redis;
  private options: Required<RateLimiterOptions>;

  constructor(options: RateLimiterOptions) {
    this.redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT || '6379'),
      retryStrategy: (times) => {
        const delay = Math.min(times * 50, 2000);
        return delay;
      }
    });

    this.options = {
      keyPrefix: 'ratelimit:',
      ...options
    };
  }

  async checkLimit(identifier: string): Promise<RateLimitResult> {
    const key = `${this.options.keyPrefix}${identifier}`;
    const now = Date.now();
    const windowStart = now - this.options.windowMs;

    try {
      // Remove old requests
      await this.redis.zremrangebyscore(key, 0, windowStart);

      // Count recent requests
      const requestCount = await this.redis.zcard(key);

      if (requestCount >= this.options.maxRequests) {
        // Get oldest request timestamp
        const oldestRequest = await this.redis.zrange(key, 0, 0, 'WITHSCORES');
        const retryAfter = Math.ceil((parseInt(oldestRequest[1]) + this.options.windowMs - now) / 1000);

        return {
          allowed: false,
          remaining: 0,
          retryAfter
        };
      }

      // Add new request
      await this.redis.zadd(key, now, `${now}:${Math.random()}`);
      // Set expiry on the key
      await this.redis.expire(key, Math.ceil(this.options.windowMs / 1000));

      return {
        allowed: true,
        remaining: this.options.maxRequests - requestCount - 1
      };
    } catch (error) {
      console.error('Rate limiter error:', error);
      // Fail open - allow request in case of Redis error
      return {
        allowed: true,
        remaining: 0
      };
    }
  }

  async disconnect(): Promise<void> {
    await this.redis.quit();
  }
} 