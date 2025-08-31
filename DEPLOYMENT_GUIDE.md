# SmartProBono Deployment Guide

## 🚀 **Complete Deployment Guide for Production**

This guide covers everything you need to deploy SmartProBono in production with optimized performance and minimal resource usage.

---

## 📋 **Pre-Deployment Checklist**

### ✅ **System Requirements**
- **OS**: macOS, Linux, or Windows with WSL
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 10GB free space
- **CPU**: Multi-core processor recommended
- **Network**: Stable internet connection

### ✅ **Dependencies Installed**
- [ ] Python 3.11+ with virtual environment
- [ ] Node.js 16+ and npm
- [ ] Ollama installed and running
- [ ] Supabase project configured
- [ ] All Python packages installed

---

## 🛠️ **Installation Steps**

### 1. **Clone and Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd SmartProBono-main

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. **Ollama Setup**
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull lightweight models
ollama pull tinyllama:1.1b
ollama pull qwen2.5:0.5b
ollama pull gemma2:2b
ollama pull llama3.2:3b
```

### 3. **Environment Configuration**
```bash
# Set up environment variables
export SUPABASE_URL="your-supabase-url"
export SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"

# Optional: Set up email configuration
export SMTP_HOST="your-smtp-host"
export SMTP_PORT="587"
export SMTP_USER="your-email"
export SMTP_PASS="your-password"
```

### 4. **Database Setup**
```bash
# Run database migrations
python3 -c "
from backend.services.database_service import DatabaseService
db = DatabaseService()
db.run_migrations()
print('✅ Database migrations completed')
"
```

---

## 🚀 **Deployment Options**

### **Option 1: Development Mode (Recommended for Testing)**
```bash
# Quick start - backend only
./quick_start.sh

# Or full system
./start_smartprobono.sh
```

### **Option 2: Lightweight Production Mode**
```bash
# Optimized for minimal resource usage
./start_lightweight.sh

# Or ultra-lightweight
./start_ultra_lightweight.sh
```

### **Option 3: Full Production Mode**
```bash
# Complete system with all features
./start_smartprobono.sh
```

---

## 🔧 **Production Configuration**

### **Backend Configuration**
```python
# In advanced_multi_agent_api.py
app.config.update({
    'DEBUG': False,
    'TESTING': False,
    'SECRET_KEY': 'your-production-secret-key'
})

# Use production WSGI server
# gunicorn -w 4 -b 0.0.0.0:8081 advanced_multi_agent_api:app
```

### **Frontend Configuration**
```bash
# Build for production
cd frontend
npm run build

# Serve with production server
npm install -g serve
serve -s build -l 3002
```

### **Ollama Production Settings**
```bash
# Create production Ollama configuration
cat > ~/.ollama/config.json << EOF
{
  "host": "0.0.0.0:11434",
  "max_loaded_models": 2,
  "max_queued_requests": 10
}
EOF
```

---

## 📊 **Performance Optimization**

### **Model Optimization**
```bash
# Create optimized models
ollama create qwen2.5-legal-optimized -f qwen2.5-legal-optimized.Modelfile
ollama create tinyllama-legal-optimized -f tinyllama-legal-optimized.Modelfile
ollama create gemma2-legal-optimized -f gemma2-legal-optimized.Modelfile
```

### **System Optimization**
```bash
# Set system limits
ulimit -n 65536  # Increase file descriptor limit
ulimit -u 32768  # Increase process limit

# Optimize memory usage
echo 'vm.swappiness=10' >> /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' >> /etc/sysctl.conf
```

### **Database Optimization**
```sql
-- Optimize Supabase settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
```

---

## 🔒 **Security Configuration**

### **Environment Security**
```bash
# Use environment files
cat > .env << EOF
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SECRET_KEY=your-secret-key
SMTP_HOST=your-smtp-host
SMTP_USER=your-email
SMTP_PASS=your-password
EOF

# Secure the file
chmod 600 .env
```

### **Network Security**
```bash
# Configure firewall (if needed)
sudo ufw allow 3002  # Frontend
sudo ufw allow 8081  # Backend
sudo ufw allow 11434 # Ollama (if external access needed)
```

### **SSL/HTTPS Setup**
```bash
# Using nginx reverse proxy
sudo apt install nginx certbot python3-certbot-nginx

# Configure nginx
sudo nano /etc/nginx/sites-available/smartprobono
```

---

## 📈 **Monitoring and Maintenance**

### **Health Monitoring**
```bash
# Set up monitoring script
cat > monitor_production.sh << 'EOF'
#!/bin/bash
while true; do
    echo "$(date): Checking services..."
    
    # Check backend
    curl -f http://localhost:8081/api/health || echo "Backend down!"
    
    # Check frontend
    curl -f http://localhost:3002 || echo "Frontend down!"
    
    # Check Ollama
    curl -f http://localhost:11434/api/tags || echo "Ollama down!"
    
    sleep 60
done
EOF

chmod +x monitor_production.sh
```

### **Log Management**
```bash
# Set up log rotation
sudo nano /etc/logrotate.d/smartprobono

# Content:
/Users/baheemferrell/Desktop/Apps/SmartProBono-main/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 baheemferrell baheemferrell
}
```

### **Backup Strategy**
```bash
# Database backup
pg_dump $SUPABASE_URL > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf smartprobono_backup_$(date +%Y%m%d).tar.gz \
    --exclude=node_modules \
    --exclude=venv \
    --exclude=*.log \
    .
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Service Won't Start**
```bash
# Check logs
tail -f backend.log
tail -f frontend.log
tail -f langgraph.log

# Check ports
lsof -i :8081
lsof -i :3002
lsof -i :11434
```

#### **High Memory Usage**
```bash
# Monitor memory
python3 monitor_performance.py

# Restart services
pkill -f advanced_multi_agent_api
pkill -f ollama
./start_lightweight.sh
```

#### **Slow Responses**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
pkill -f ollama
ollama serve

# Use smaller models
curl -X POST http://localhost:8081/api/legal/chat \
  -d '{"message": "test", "task_type": "tiny"}'
```

#### **Database Connection Issues**
```bash
# Test Supabase connection
python3 -c "
from backend.services.database_service import DatabaseService
db = DatabaseService()
print('✅ Database connection OK')
"
```

---

## 📊 **Performance Benchmarks**

### **Expected Performance**
- **Response Time**: 2-5 seconds
- **Memory Usage**: < 2GB total
- **CPU Usage**: < 70%
- **Concurrent Users**: 10-50 (depending on hardware)
- **Uptime**: 99%+ with proper monitoring

### **Load Testing**
```bash
# Simple load test
for i in {1..10}; do
    curl -X POST http://localhost:8081/api/legal/chat \
      -H "Content-Type: application/json" \
      -d '{"message": "Test message '${i}'", "task_type": "chat"}' &
done
wait
```

---

## 🔄 **Updates and Maintenance**

### **Regular Maintenance Tasks**
```bash
# Weekly tasks
./update_system.sh

# Monthly tasks
./backup_data.sh
./optimize_database.sh
./update_models.sh
```

### **Update Process**
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt
cd frontend && npm install

# Restart services
./restart_services.sh
```

---

## 📞 **Support and Resources**

### **Documentation**
- [Model Optimization Guide](MODEL_OPTIMIZATION_GUIDE.md)
- [Performance Guide](PERFORMANCE_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)

### **Monitoring Tools**
- `python3 monitor_performance.py` - System performance
- `python3 test_frontend_integration.py` - Integration testing
- `python3 optimize_models.py` - Model optimization

### **Emergency Contacts**
- System Admin: [Your Contact]
- Database Admin: [Your Contact]
- Technical Support: [Your Contact]

---

## ✅ **Deployment Checklist**

### **Pre-Launch**
- [ ] All services tested and working
- [ ] Performance benchmarks met
- [ ] Security configurations applied
- [ ] Monitoring systems active
- [ ] Backup procedures tested
- [ ] SSL certificates installed
- [ ] Domain configured
- [ ] Load balancer configured (if needed)

### **Post-Launch**
- [ ] Monitor system performance
- [ ] Check error logs daily
- [ ] Verify backup procedures
- [ ] Update documentation
- [ ] Plan for scaling

---

## 🎉 **Congratulations!**

Your SmartProBono system is now ready for production deployment with:
- ✅ Optimized performance
- ✅ Minimal resource usage
- ✅ Smart model selection
- ✅ Comprehensive monitoring
- ✅ Production-ready configuration

**Next Steps:**
1. Deploy to your production environment
2. Monitor system performance
3. Scale as needed
4. Continue development and improvements

Happy deploying! 🚀
