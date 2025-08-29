# SmartProBono Standalone App Deployment

## 🚀 Quick Deploy to Render

The standalone app is designed for easy deployment with minimal dependencies.

### Files for Deployment:
- `app_standalone.py` - Main application
- `requirements_standalone.txt` - Minimal dependencies
- `render.yaml` - Render deployment config
- `Procfile` - Process configuration

### Deploy Steps:

1. **Push to GitHub** (already done ✅)

2. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements_standalone.txt`
     - **Start Command**: `python3 app_standalone.py`
     - **Environment**: Python 3
     - **Plan**: Free

3. **Environment Variables** (optional):
   - `PORT` - Will be set automatically by Render
   - `SUPABASE_URL` - Already configured in app
   - `SUPABASE_SERVICE_KEY` - Already configured in app

### Why This Works:

**Minimal Dependencies:**
- Only Flask, CORS, requests, and built-in Python modules
- No complex packages like gevent, websockets, or database drivers
- Compatible with Python 3.13

**Standalone Design:**
- No external database connections
- Uses Supabase REST API
- Self-contained AI service
- No complex middleware

### Testing Locally:

```bash
# Install dependencies
pip install -r requirements_standalone.txt

# Run the app
python3 app_standalone.py

# Test endpoints
curl http://localhost:8081/api/health
```

### Features Available:
- ✅ Legal Chat with AI agents
- ✅ Beta signup
- ✅ Feedback collection
- ✅ Document endpoints
- ✅ Supabase integration
- ✅ CORS enabled for frontend

The standalone app is production-ready and will deploy successfully on Render! 🎉
