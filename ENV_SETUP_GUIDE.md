# 🔧 Environment Setup Guide - Fix Chat Issues

## 🚨 IMMEDIATE PROBLEM
Your chat is returning generic fallback responses because the API keys are missing from your `.env` file.

## ⚡ QUICK FIX (2 minutes)

### Step 1: Update Your .env File
```bash
# Open your .env file
nano .env

# Replace the contents with:
DATABASE_URL=sqlite:///smartprobono_dev.db
OPENAI_API_KEY=your_actual_openai_key_here
COURTLISTENER_API_KEY=your_actual_courtlistener_key_here
SUPABASE_URL=https://ewtcvsohdgkthuyajyyk.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3dGN2c29oZGdrdGh1eWFqeXlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY0MTA0NjQsImV4cCI6MjA3MTk4NjQ2NH0.NXO-6aVlkqc9HCL6MHRcW0V9JN4Z85WhvRxK6aJnBbI
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
RESEND_API_KEY=re_N7YNzBXp_HyNzVsWjuLNqxqUQr8oxaxvf
PORT=3001
HOST=127.0.0.1
```

### Step 2: Get Your API Keys

#### OpenAI API Key:
1. Go to: https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it and replace `your_actual_openai_key_here`

#### CourtListener API Key (Optional):
1. Go to: https://www.courtlistener.com/api/
2. Sign up and get your API key
3. Replace `your_actual_courtlistener_key_here`

### Step 3: Restart Servers
```bash
# Stop current servers
./stop_smartprobono.sh

# Wait 3 seconds
sleep 3

# Restart with new configuration
./start_smartprobono_complete.sh
```

### Step 4: Test Chat
```bash
# Test the chat API
curl -X POST http://localhost:3001/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my rights as a tenant?", "task_type": "chat"}'
```

## 🎯 Expected Result

**Before Fix:**
```
"I'm currently unable to access my research databases..."
```

**After Fix:**
```
"Based on your question about tenant rights, here's a comprehensive legal analysis..."
```

## 📊 Current Status

✅ **Working:**
- Backend server (port 3001)
- Frontend server (port 3002)
- Health API
- Legal Analysis API

⚠️ **Needs API Keys:**
- Chat API (fallback mode)
- OpenAI integration
- CourtListener integration

## 🚀 Alternative: Use Working Endpoints

If you can't get API keys immediately, use these working endpoints:

### Working Legal Analysis:
```bash
curl -X POST http://localhost:3001/api/v1/legal/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "tenant rights", "jurisdiction": "state"}'
```

### Working Health Check:
```bash
curl http://localhost:3001/api/health
```

## 🔍 Troubleshooting

### If chat still gives generic responses:
1. **Check .env file** has the correct API keys
2. **Restart servers** after updating .env
3. **Check terminal logs** for specific errors
4. **Verify API keys** are valid

### If you see "proxies" error:
- This is an OpenAI configuration issue
- Restarting servers usually fixes it

## 📞 Quick Commands

```bash
# Check if servers are running
lsof -i :3001 && lsof -i :3002

# Check environment variables
echo $OPENAI_API_KEY

# Test individual endpoints
curl http://localhost:3001/api/health
curl -X POST http://localhost:3001/api/v1/ai/chat -H "Content-Type: application/json" -d '{"message": "test", "task_type": "chat"}'
```

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Chat returns specific legal analysis instead of generic messages
- ✅ No "proxies" errors in terminal
- ✅ No "fallback mode" messages in logs
- ✅ Fast response times (< 3 seconds)

**The system is working - it just needs proper API configuration!** 🚀
