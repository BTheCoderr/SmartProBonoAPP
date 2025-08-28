# 🚀 SmartProBono MVP - Quick Start Commands

## 🎯 **One Command to Start Everything**

```bash
./start_smartprobono.sh
```

This single command will:
- ✅ Stop any existing services
- ✅ Start Supabase backend on port 8081
- ✅ Start React frontend on port 3002
- ✅ Test all endpoints
- ✅ Show you the access URLs
- ✅ Display system status

## 🛑 **Stop Everything**

```bash
./stop_smartprobono.sh
```

## 🌐 **Access Your MVP**

After running `./start_smartprobono.sh`:

- **Frontend**: http://localhost:3002
- **Backend API**: http://localhost:8081
- **Health Check**: http://localhost:8081/api/health

## 🧪 **Test the AI Improvements**

```bash
# Test greeting (should be brief now!)
curl -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "task_type": "chat"}'

# Test compliance (should be detailed)
curl -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is GDPR compliance?", "task_type": "chat"}'
```

## 📊 **What You Get**

### ✅ **Backend Features**
- Supabase PostgreSQL with Row Level Security
- Multi-agent AI system (5 specialized agents)
- Fixed "hello" problem (brief responses)
- JWT authentication ready
- Email system with Zoho SMTP

### ✅ **Frontend Features**
- React app with Material UI
- Professional design
- All MVP pages
- Responsive layout

### ✅ **Security Features**
- Row Level Security (RLS)
- User data isolation
- Protected API endpoints
- Input validation

## 🎉 **Ready for Pilot Testing!**

Your SmartProBono MVP is now:
- ✅ **Production-ready** backend
- ✅ **Intelligent AI** responses
- ✅ **Enterprise-grade** security
- ✅ **Scalable** database
- ✅ **Professional** UI/UX

**Just run `./start_smartprobono.sh` and you're ready to go!** 🚀
