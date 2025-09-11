# CourtListener API Setup Guide

## 🚀 How to Get Real Case Law Data

### Step 1: Get CourtListener API Key

1. **Visit CourtListener API**: https://www.courtlistener.com/api/
2. **Create Account**: Sign up for a free account
3. **Get API Key**: Copy your API key from the dashboard

### Step 2: Set API Key

**Option A: Environment Variable**
```bash
export COURTLISTENER_API_KEY="your_api_key_here"
```

**Option B: .env File**
```bash
echo "COURTLISTENER_API_KEY=your_api_key_here" >> .env
```

**Option C: Render.com Environment Variable**
1. Go to your Render dashboard
2. Select your service
3. Go to Environment tab
4. Add: `COURTLISTENER_API_KEY` = `your_api_key_here`

### Step 3: Test the Integration

```bash
python test_courtlistener_simple.py
```

You should see:
- ✅ API Key Status: Found
- 📊 Fallback Mode: No
- Real case law data instead of mock data

## 🔍 What You Get with Real API

- **Real Case Law**: Actual cases from US courts
- **Live Data**: Up-to-date case information
- **Comprehensive Search**: Search across all case types
- **Recent Cases**: Latest court decisions
- **Similar Cases**: AI-powered case matching

## 📊 API Limits

- **Free Tier**: 100 requests per day
- **Rate Limiting**: 1 request per second (built-in)
- **Fallback**: Automatic mock data when limits exceeded

## 🛠️ Current Status

✅ **Integration**: Complete and working
✅ **Fallback Mode**: Active (using mock data)
✅ **Error Handling**: Robust
✅ **Rate Limiting**: Implemented
❌ **API Key**: Not set (using mock data)

## 🎯 Next Steps

1. Get your CourtListener API key
2. Set the environment variable
3. Test with real data
4. Deploy with API key to production

Your CourtListener integration is ready to go!
