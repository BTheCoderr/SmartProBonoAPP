class AttorneyCache {
  constructor() {
    this.cache = new Map();
    this.timeouts = new Map();
    this.CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
  }

  generateKey(filters = {}) {
    return JSON.stringify(filters);
  }

  get(filters = {}) {
    const key = this.generateKey(filters);
    const cached = this.cache.get(key);

    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      return cached.data;
    }

    return null;
  }

  set(filters = {}, data) {
    const key = this.generateKey(filters);
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    });

    // Set expiration
    if (this.timeouts.has(key)) {
      clearTimeout(this.timeouts.get(key));
    }

    this.timeouts.set(
      key,
      setTimeout(() => {
        this.cache.delete(key);
        this.timeouts.delete(key);
      }, this.CACHE_DURATION)
    );
  }

  invalidate(filters = {}) {
    if (filters) {
      const key = this.generateKey(filters);
      this.cache.delete(key);
      if (this.timeouts.has(key)) {
        clearTimeout(this.timeouts.get(key));
        this.timeouts.delete(key);
      }
    } else {
      // Invalidate all cache
      this.cache.clear();
      this.timeouts.forEach(timeout => clearTimeout(timeout));
      this.timeouts.clear();
    }
  }
}

export const attorneyCache = new AttorneyCache();
export default attorneyCache;
