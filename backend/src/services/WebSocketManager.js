const { Server } = require('socket.io');
const Redis = require('ioredis');

class WebSocketManager {
  constructor(server) {
    this.setupWebSocket(server);
    this.setupRedis();
    this.activeUsers = new Map();
    this.userSessions = new Map();
    this.setupSocketHandlers();
  }

  setupWebSocket(server) {
    this.io = new Server(server, {
      cors: {
        origin: process.env.FRONTEND_URL || 'http://localhost:3000',
        methods: ['GET', 'POST']
      },
      pingTimeout: 60000,
      pingInterval: 25000
    });
  }

  setupRedis() {
    this.redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379,
      retryStrategy: (times) => {
        const delay = Math.min(times * 50, 2000);
        return delay;
      },
      maxRetriesPerRequest: 3
    });

    this.redis.on('error', (error) => {
      console.error('Redis connection error:', error);
    });
  }

  async safeRedisOperation(operation) {
    try {
      return await operation();
    } catch (error) {
      console.error('Redis operation failed:', error);
      throw new Error('Analytics operation failed');
    }
  }

  setupSocketHandlers() {
    this.io.on('connection', (socket) => {
      console.log('Client connected:', socket.id);

      this.setupEventHandlers(socket);
      this.setupErrorHandling(socket);
      this.setupDisconnectHandler(socket);
    });
  }

  setupEventHandlers(socket) {
    const handlers = {
      'join_form': (formType) => this.handleJoinForm(socket, formType),
      'leave_form': (formType) => this.handleLeaveForm(socket, formType),
      'form_view': (data) => this.handleFormView(socket, data),
      'form_start': (data) => this.handleFormStart(socket, data),
      'form_completion': (data) => this.handleFormCompletion(socket, data),
      'field_interaction': (data) => this.handleFieldInteraction(socket, data)
    };

    Object.entries(handlers).forEach(([event, handler]) => {
      socket.on(event, async (data) => {
        try {
          await handler(data);
        } catch (error) {
          console.error(`Error handling ${event}:`, error);
          socket.emit('error', { message: `Failed to process ${event}` });
        }
      });
    });
  }

  setupErrorHandling(socket) {
    socket.on('error', (error) => {
      console.error('Socket error:', error);
    });
  }

  setupDisconnectHandler(socket) {
    socket.on('disconnect', async () => {
      try {
        await this.handleDisconnect(socket);
      } catch (error) {
        console.error('Error handling disconnect:', error);
      }
    });
  }

  async handleJoinForm(socket, formType) {
    try {
      socket.join(`form:${formType}`);
      
      if (!this.activeUsers.has(formType)) {
        this.activeUsers.set(formType, new Set());
      }
      this.activeUsers.get(formType).add(socket.id);

      this.userSessions.set(socket.id, {
        formType,
        startTime: Date.now(),
        interactions: [],
        completedFields: new Set(),
        lastActivity: Date.now()
      });

      await this.broadcastActiveUsers(formType);
    } catch (error) {
      console.error('Error in handleJoinForm:', error);
      socket.emit('error', { message: 'Failed to join form session' });
    }
  }

  async handleLeaveForm(socket, formType) {
    socket.leave(`form:${formType}`);
    
    if (this.activeUsers.has(formType)) {
      this.activeUsers.get(formType).delete(socket.id);
      this.broadcastActiveUsers(formType);
    }

    // Save session data if exists
    const session = this.userSessions.get(socket.id);
    if (session) {
      await this.saveSessionData(socket.id, formType);
      this.userSessions.delete(socket.id);
    }
  }

  async handleFormView(socket, data) {
    const { formType } = data;
    await this.incrementMetric(`${formType}:views`);
    await this.trackUserBehavior(socket.id, 'view', data);
    this.broadcastAnalyticsUpdate(formType);
  }

  async handleFormStart(socket, data) {
    const { formType } = data;
    await this.incrementMetric(`${formType}:starts`);
    await this.trackUserBehavior(socket.id, 'start', data);
    this.broadcastAnalyticsUpdate(formType);
  }

  async handleFormCompletion(socket, data) {
    const { formType, completionTime, formData } = data;
    
    await this.redis.lpush(`${formType}:completions`, JSON.stringify({
      timestamp: new Date().toISOString(),
      completionTime,
      formData,
      sessionData: this.userSessions.get(socket.id)
    }));

    await Promise.all([
      this.incrementMetric(`${formType}:completed`),
      this.updateAverageCompletionTime(formType, completionTime),
      this.trackUserBehavior(socket.id, 'completion', data)
    ]);

    this.broadcastAnalyticsUpdate(formType);
    this.broadcastFormActivity(formType, 'completion', data);
  }

  async handleFieldInteraction(socket, data) {
    const { formType, fieldName, isValid, value } = data;
    const session = this.userSessions.get(socket.id);
    
    if (session) {
      session.interactions.push({
        fieldName,
        timestamp: Date.now(),
        isValid,
        value: typeof value === 'string' ? value.length : null
      });

      if (isValid) {
        session.completedFields.add(fieldName);
      }

      session.lastActivity = Date.now();
    }

    await Promise.all([
      this.redis.hincrby(`${formType}:field_interactions`, fieldName, 1),
      isValid ? null : this.redis.hincrby(`${formType}:field_errors`, fieldName, 1),
      this.trackFieldTiming(formType, fieldName, data.duration),
      this.trackUserBehavior(socket.id, 'field_interaction', data)
    ]);

    this.broadcastAnalyticsUpdate(formType);
  }

  async handleDisconnect(socket) {
    for (const [formType, users] of this.activeUsers.entries()) {
      if (users.has(socket.id)) {
        users.delete(socket.id);
        await this.saveSessionData(socket.id, formType);
        this.broadcastActiveUsers(formType);
      }
    }
    this.userSessions.delete(socket.id);
  }

  // Enhanced helper methods
  async saveSessionData(socketId, formType) {
    const session = this.userSessions.get(socketId);
    if (!session) return;

    try {
      const sessionData = {
        ...session,
        endTime: Date.now(),
        duration: Date.now() - session.startTime,
        completedFields: Array.from(session.completedFields),
        completionRate: session.completedFields.size / (await this.getFormFieldCount(formType))
      };

      await this.safeRedisOperation(() => 
        this.redis.lpush(`${formType}:sessions`, JSON.stringify(sessionData))
      );
      await this.updateSessionMetrics(formType, sessionData);
    } catch (error) {
      console.error('Error saving session data:', error);
    }
  }

  async updateSessionMetrics(formType, sessionData) {
    const { duration, completionRate, interactions } = sessionData;

    await Promise.all([
      this.redis.lpush(`${formType}:session_durations`, duration),
      this.redis.lpush(`${formType}:completion_rates`, completionRate),
      this.updateAverageSessionDuration(formType, duration),
      this.updateFieldProgressionMetrics(formType, interactions)
    ]);
  }

  async trackUserBehavior(socketId, eventType, data) {
    const session = this.userSessions.get(socketId);
    if (!session) return;

    const behaviorData = {
      timestamp: Date.now(),
      eventType,
      data,
      sessionDuration: Date.now() - session.startTime
    };

    await this.redis.lpush(`${session.formType}:user_behavior`, JSON.stringify(behaviorData));
  }

  async getFormFieldCount(formType) {
    const fieldCount = await this.redis.get(`${formType}:field_count`);
    return parseInt(fieldCount) || 0;
  }

  async updateFieldProgressionMetrics(formType, interactions) {
    const progressionKey = `${formType}:field_progression`;
    
    for (let i = 0; i < interactions.length - 1; i++) {
      const currentField = interactions[i].fieldName;
      const nextField = interactions[i + 1].fieldName;
      await this.redis.hincrby(progressionKey, `${currentField}:${nextField}`, 1);
    }
  }

  async updateAverageSessionDuration(formType, newDuration) {
    const key = `${formType}:avg_session_duration`;
    const count = await this.redis.llen(`${formType}:session_durations`);
    const currentAvg = await this.redis.get(key) || 0;
    
    const newAvg = Math.round(
      (parseInt(currentAvg) * (count - 1) + newDuration) / count
    );
    
    await this.redis.set(key, newAvg);
  }

  // Existing methods remain the same...
  async incrementMetric(key) {
    await this.redis.incr(key);
  }

  async updateAverageCompletionTime(formType, newTime) {
    const key = `${formType}:avg_completion_time`;
    const count = await this.redis.get(`${formType}:completed`) || 1;
    const currentAvg = await this.redis.get(key) || 0;
    
    const newAvg = Math.round(
      (currentAvg * (count - 1) + newTime) / count
    );
    
    await this.redis.set(key, newAvg);
  }

  broadcastActiveUsers(formType) {
    const count = this.activeUsers.get(formType)?.size || 0;
    this.io.to(`form:${formType}`).emit('analytics_update', {
      formType,
      metrics: { activeUsers: count }
    });
  }

  async broadcastAnalyticsUpdate(formType) {
    const metrics = await this.getFormMetrics(formType);
    this.io.to(`form:${formType}`).emit('analytics_update', {
      formType,
      metrics
    });
  }

  broadcastFormActivity(formType, activityType, data) {
    this.io.to(`form:${formType}`).emit('form_activity', {
      formType,
      activityType,
      data,
      timestamp: new Date().toISOString()
    });
  }

  async getFormMetrics(formType) {
    try {
      const [
        views,
        starts,
        completed,
        avgCompletionTime,
        avgSessionDuration,
        fieldInteractions,
        fieldErrors,
        sessionData,
        userBehavior
      ] = await Promise.all([
        this.safeRedisOperation(() => this.redis.get(`${formType}:views`)),
        this.safeRedisOperation(() => this.redis.get(`${formType}:starts`)),
        this.safeRedisOperation(() => this.redis.get(`${formType}:completed`)),
        this.safeRedisOperation(() => this.redis.get(`${formType}:avg_completion_time`)),
        this.safeRedisOperation(() => this.redis.get(`${formType}:avg_session_duration`)),
        this.safeRedisOperation(() => this.redis.hgetall(`${formType}:field_interactions`)),
        this.safeRedisOperation(() => this.redis.hgetall(`${formType}:field_errors`)),
        this.safeRedisOperation(() => this.redis.lrange(`${formType}:sessions`, 0, 9)),
        this.safeRedisOperation(() => this.redis.lrange(`${formType}:user_behavior`, 0, 49))
      ]);

      return {
        views: parseInt(views) || 0,
        starts: parseInt(starts) || 0,
        completed: parseInt(completed) || 0,
        averageCompletionTime: parseInt(avgCompletionTime) || 0,
        averageSessionDuration: parseInt(avgSessionDuration) || 0,
        fieldInteractions: this.parseRedisHash(fieldInteractions),
        fieldErrors: this.parseRedisHash(fieldErrors),
        recentSessions: sessionData.map(JSON.parse),
        recentBehavior: userBehavior.map(JSON.parse)
      };
    } catch (error) {
      console.error('Error getting form metrics:', error);
      return {
        views: 0,
        starts: 0,
        completed: 0,
        averageCompletionTime: 0,
        averageSessionDuration: 0,
        fieldInteractions: {},
        fieldErrors: {},
        recentSessions: [],
        recentBehavior: []
      };
    }
  }

  parseRedisHash(hash) {
    if (!hash) return {};
    return Object.fromEntries(
      Object.entries(hash).map(([key, value]) => [key, parseInt(value)])
    );
  }
}

module.exports = WebSocketManager; 