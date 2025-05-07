const WebSocketManager = require('../../services/WebSocketManager');
const Redis = require('ioredis');
const { createServer } = require('http');
const Client = require('socket.io-client');

jest.mock('ioredis');

describe('WebSocketManager', () => {
  let httpServer;
  let wsManager;
  let clientSocket;
  let mockRedis;

  beforeAll((done) => {
    httpServer = createServer();
    wsManager = new WebSocketManager(httpServer);
    httpServer.listen(() => {
      const port = httpServer.address().port;
      clientSocket = new Client(`http://localhost:${port}`);
      clientSocket.on('connect', done);
    });
  });

  beforeEach(() => {
    mockRedis = {
      incr: jest.fn().mockResolvedValue(1),
      get: jest.fn().mockResolvedValue('0'),
      set: jest.fn().mockResolvedValue('OK'),
      lpush: jest.fn().mockResolvedValue(1),
      hincrby: jest.fn().mockResolvedValue(1),
      hgetall: jest.fn().mockResolvedValue({}),
    };

    Redis.mockImplementation(() => mockRedis);
  });

  afterAll(() => {
    wsManager.io.close();
    clientSocket.close();
    httpServer.close();
  });

  describe('connection handling', () => {
    it('should handle client connection', (done) => {
      const newClient = new Client(`http://localhost:${httpServer.address().port}`);
      newClient.on('connect', () => {
        expect(newClient.connected).toBe(true);
        newClient.close();
        done();
      });
    });
  });

  describe('form room management', () => {
    const mockFormType = 'test_form';

    it('should handle joining a form room', (done) => {
      clientSocket.emit('join_form', mockFormType);

      // Wait for analytics update with active users
      clientSocket.on('analytics_update', (data) => {
        expect(data.formType).toBe(mockFormType);
        expect(data.metrics.activeUsers).toBe(1);
        done();
      });
    });

    it('should handle leaving a form room', (done) => {
      // First join
      clientSocket.emit('join_form', mockFormType);

      // Then leave
      clientSocket.emit('leave_form', mockFormType);

      // Wait for analytics update with zero active users
      clientSocket.on('analytics_update', (data) => {
        if (data.metrics.activeUsers === 0) {
          expect(data.formType).toBe(mockFormType);
          done();
        }
      });
    });
  });

  describe('analytics tracking', () => {
    const mockFormType = 'test_form';

    it('should track form views', (done) => {
      const mockData = {
        formType: mockFormType,
        timestamp: new Date().toISOString()
      };

      clientSocket.emit('form_view', mockData);

      setTimeout(() => {
        expect(mockRedis.incr).toHaveBeenCalledWith(`${mockFormType}:views`);
        done();
      }, 100);
    });

    it('should track form completion', (done) => {
      const mockData = {
        formType: mockFormType,
        completionTime: 5000,
        formData: {
          fieldCount: 5,
          filledFields: 5
        }
      };

      clientSocket.emit('form_completion', mockData);

      setTimeout(() => {
        expect(mockRedis.lpush).toHaveBeenCalledWith(
          `${mockFormType}:completions`,
          expect.any(String)
        );
        expect(mockRedis.incr).toHaveBeenCalledWith(`${mockFormType}:completed`);
        done();
      }, 100);
    });

    it('should track field interactions', (done) => {
      const mockData = {
        formType: mockFormType,
        fieldName: 'test_field',
        isValid: true
      };

      clientSocket.emit('field_interaction', mockData);

      setTimeout(() => {
        expect(mockRedis.hincrby).toHaveBeenCalledWith(
          `${mockFormType}:field_interactions`,
          'test_field',
          1
        );
        done();
      }, 100);
    });
  });

  describe('metrics calculation', () => {
    const mockFormType = 'test_form';

    it('should calculate average completion time correctly', async () => {
      mockRedis.get
        .mockResolvedValueOnce('2') // completed count
        .mockResolvedValueOnce('1000'); // current average

      await wsManager.updateAverageCompletionTime(mockFormType, 2000);

      expect(mockRedis.set).toHaveBeenCalledWith(
        `${mockFormType}:avg_completion_time`,
        1500 // (1000 * 1 + 2000) / 2
      );
    });

    it('should aggregate form metrics', async () => {
      mockRedis.get
        .mockResolvedValueOnce('10') // views
        .mockResolvedValueOnce('8')  // starts
        .mockResolvedValueOnce('5')  // completed
        .mockResolvedValueOnce('3000'); // avg completion time

      mockRedis.hgetall
        .mockResolvedValueOnce({ // field interactions
          'field1': '10',
          'field2': '8'
        })
        .mockResolvedValueOnce({ // field errors
          'field1': '2',
          'field2': '1'
        });

      const metrics = await wsManager.getFormMetrics(mockFormType);

      expect(metrics).toEqual({
        views: 10,
        starts: 8,
        completed: 5,
        averageCompletionTime: 3000,
        fieldInteractions: {
          field1: 10,
          field2: 8
        },
        fieldErrors: {
          field1: 2,
          field2: 1
        }
      });
    });
  });
}); 