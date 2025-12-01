# 🚀 Setup Groq API - For Lightning Fast Responses!

## Why Groq?

SmartProBono Lite uses Groq because it's **MUCH FASTER** than other AI models:

| AI Service | Response Time | Quality | Cost |
|------------|---------------|---------|------|
| **Groq** | **< 1 second** ⚡ | Excellent | FREE |
| Ollama (Local) | 5-15 seconds | Good | FREE |
| Saul Legal AI | 8-12 seconds | Technical | FREE |
| Gemini | 2-5 seconds | Excellent | FREE |
| OpenAI GPT-4 | 3-8 seconds | Excellent | $20+/month |

**Groq makes your chat feel instant and snappy!**

---

## 🎯 Get Your Free Groq API Key (2 minutes)

### Step 1: Sign Up
1. Go to: https://console.groq.com/
2. Click **"Sign Up"** or **"Get Started"**
3. Sign up with Google/GitHub or email
4. Verify your email

### Step 2: Create API Key
1. Once logged in, go to: https://console.groq.com/keys
2. Click **"Create API Key"**
3. Give it a name (e.g., "SmartProBono")
4. Copy your API key (starts with `gsk_...`)

⚠️ **Important**: Save this key somewhere safe - you won't be able to see it again!

### Step 3: Add to Your .env File
```bash
# Open your .env file
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
nano .env

# Add this line (replace with your actual key):
GROQ_API_KEY=gsk_your_actual_groq_key_here

# Save: Ctrl+X, then Y, then Enter
```

---

## 📊 Groq Free Tier Limits

### What You Get FREE:
- ✅ **14,400 requests/day** per model
- ✅ **30 requests/minute** per model
- ✅ **6,000 tokens/minute**
- ✅ **No credit card required**
- ✅ **Multiple models available**

### Groq Models Available:
- `llama-3.1-70b-versatile` - Best quality, conversational
- `llama-3.1-8b-instant` - Fastest, good for chat
- `mixtral-8x7b-32768` - Good balance
- `gemma2-9b-it` - Efficient

**This is MORE than enough for development and testing!**

---

## 🔧 How I've Set It Up

Once you add your Groq API key, the system will:

1. **Use Groq for conversational chat** (fast, < 1 second)
2. **Use Saul for detailed legal analysis** (when needed)
3. **Use Ollama as fallback** (if Groq is down)
4. **Use Gemini for complex research** (backup option)

**Priority Order**:
```
User Message
    ↓
Groq (if key present) → FAST! < 1 second
    ↓ (if Groq unavailable)
Gemini → Good quality, 2-5 seconds
    ↓ (if Gemini unavailable)
Ollama → Local, always available, 5-15 seconds
```

---

## ✅ After Adding Groq Key

### Restart Backend:
```bash
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
./stop_ai_servers.sh
./start_ai_servers.sh
```

### Test It:
```bash
# Test with Groq (should be FAST!)
curl -X POST http://localhost:3001/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hey", "task_type": "legal"}'

# Watch the response time - should be < 1 second!
```

---

## 🎯 Expected Results

### WITHOUT Groq (Current):
```
Response time: 8-12 seconds
Model used: saul or ollama
User experience: Feels slow 😴
```

### WITH Groq:
```
Response time: < 1 second ⚡
Model used: groq
User experience: Feels instant! 🚀
```

---

## 📊 Cost Comparison

| Setup | Daily Requests | Cost/Month | Response Time |
|-------|----------------|------------|---------------|
| **Groq Only** | 14,400 | **$0** | < 1 sec |
| **Current (Ollama/Saul)** | Unlimited | $0 | 5-15 sec |
| **Groq + Fallbacks** | 14,400+ | **$0** | < 1 sec (with backup) |
| **OpenAI GPT-4** | Varies | $20-50 | 3-8 sec |

**Best option: Groq with your current models as fallback = $0/month + lightning fast!**

---

## 🔍 Verify Groq is Working

After adding your key and restarting:

```bash
# Check status
./diagnose_ai.sh

# Should show:
✅ Groq API: Configured
✅ Gemini API: Configured
✅ Ollama: Running

# Test response time
time curl -X POST http://localhost:3001/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hey", "task_type": "legal"}'

# Should complete in < 2 seconds (including network time)
```

---

## 💡 Pro Tips

### 1. Rate Limits
If you hit Groq's limits (unlikely for dev):
- System automatically falls back to Gemini or Ollama
- No errors, just slightly slower responses

### 2. Best Models for Each Task
```python
Conversational chat → llama-3.1-8b-instant (fastest)
Legal analysis → llama-3.1-70b-versatile (best quality)
Document review → mixtral-8x7b-32768 (good balance)
```

### 3. Monitor Usage
Check usage at: https://console.groq.com/settings/usage

---

## 🚀 Get Started Now

1. **Get Groq API Key**: https://console.groq.com/keys
2. **Add to .env**: `GROQ_API_KEY=gsk_your_key_here`
3. **Restart servers**: `./start_ai_servers.sh`
4. **Test**: Open http://localhost:3002/legal-chat
5. **Enjoy lightning-fast responses!** ⚡

---

## ❓ Troubleshooting

### "Groq API key invalid"
- Make sure key starts with `gsk_`
- Check for extra spaces in .env file
- Get a new key from https://console.groq.com/keys

### "Still using Ollama"
- Restart backend server
- Check .env file has `GROQ_API_KEY=gsk_...`
- Run `./diagnose_ai.sh` to verify config

### "Rate limit exceeded"
- Normal if testing heavily
- System falls back to other models automatically
- Limits reset every minute/day

---

## 🎉 Why This is Better

✅ **10x faster responses** (< 1 sec vs 5-15 sec)
✅ **Better user experience** (feels instant)
✅ **Still free** ($0/month)
✅ **Fallback safety** (if Groq down, uses others)
✅ **Like SmartProBono Lite** (same speed & quality)

**Just like SmartProBono Lite, but with MORE options!**

---

**Get your free Groq API key now and make your chat lightning fast!** ⚡

