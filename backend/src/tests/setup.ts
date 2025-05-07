import { RedisCluster } from '../config/redis';

beforeAll(async () => {
  // Mock Redis for tests
  jest.mock('ioredis', () => {
    const Redis = jest.requireActual('ioredis');
    return {
      ...Redis,
      Cluster: jest.fn().mockImplementation(() => ({
        on: jest.fn(),
        ping: jest.fn().mockResolvedValue('PONG'),
        get: jest.fn().mockResolvedValue('test-value'),
        set: jest.fn().mockResolvedValue('OK'),
        hget: jest.fn().mockResolvedValue('test-hash-value'),
        hset: jest.fn().mockResolvedValue(1),
        zadd: jest.fn().mockResolvedValue(1),
        zcard: jest.fn().mockResolvedValue(0),
        zrange: jest.fn().mockResolvedValue(['test:1234567890']),
        zremrangebyscore: jest.fn().mockResolvedValue(1),
        expire: jest.fn().mockResolvedValue(1),
        quit: jest.fn().mockResolvedValue('OK')
      }))
    };
  });
});

afterAll(async () => {
  await RedisCluster.closeConnection();
}); 