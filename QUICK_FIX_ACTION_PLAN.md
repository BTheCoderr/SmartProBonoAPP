# 🚀 Quick Fix Action Plan - Get SmartProBono Running!

## 🚨 **Immediate Issues (Fix in Next 30 Minutes)**

### **1. Stop Conflicting Services**
```bash
# Kill ControlCenter on port 5000
sudo lsof -ti:5000 | xargs kill -9

# Kill Lozada Languages on port 3000  
sudo lsof -ti:3000 | xargs kill -9

# Verify ports are clear
lsof -i :3000 -i :5000
```

### **2. Start Working Backend**
```bash
# Use the working script
./run_with_email_alt.sh

# Wait 10 seconds, then test
sleep 10
curl http://localhost:8081/api/health
```

### **3. Verify Frontend-Backend Connection**
```bash
# Test backend API
curl http://localhost:8081/api/beta/signup -X POST -H "Content-Type: application/json" -d '{"email":"test@example.com"}'

# Test frontend
curl http://localhost:3002 | grep -i "smartprobono"
```

## ✅ **What Should Work After Fixes**

1. **Frontend**: http://localhost:3002 (SmartProBono landing page)
2. **Backend**: http://localhost:8081/api/health (API health check)
3. **Email**: Test with `python test_email.py`
4. **Full Stack**: Frontend can communicate with backend

## 🔧 **If Backend Still Won't Start**

### **Alternative Backend Approach**
```bash
# Use simple working backend
cd backend
source ../venv/bin/activate
python simple_app.py

# This runs on port 5002
curl http://localhost:5002/api/health
```

### **Update Frontend Proxy**
```bash
# Edit frontend/package.json
# Change "proxy": "http://localhost:8081" to "proxy": "http://localhost:5002"
```

## 📋 **Quick Test Checklist**

- [ ] Port 3000 is free (no Lozada Languages)
- [ ] Port 5000 is free (no ControlCenter)  
- [ ] Backend running on port 8081 or 5002
- [ ] Frontend running on port 3002
- [ ] Email system working (`python test_email.py`)
- [ ] Frontend can reach backend API
- [ ] Beta signup form works
- [ ] Legal AI chat accessible

## 🎯 **Success Criteria**

**System is working when:**
1. Frontend loads SmartProBono landing page
2. Backend responds to health check
3. Email system sends test emails
4. No port conflicts or errors
5. All documented features accessible

## 🚀 **Next Steps After Fix**

1. **Test All Features** - Run through TESTING_CHECKLIST.md
2. **Update Documentation** - Mark working vs. broken features
3. **Plan Backend Fix** - Address dependency issues
4. **User Testing** - Test with real users

---

**Time Estimate**: 30 minutes to get basic system running
**Priority**: HIGH - Get system functional first, optimize later
**Status**: Ready to implement fixes
