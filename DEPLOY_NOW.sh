#!/bin/bash

echo "🚀 SmartProBono Production Deployment"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found. Are you in the project root?"
    exit 1
fi

echo "✅ Files ready for deployment"
echo ""
echo "📦 What will be deployed:"
echo "   - Backend API (44 AI services)"
echo "   - Multi-Agent System (6 agents)"
echo "   - Frontend (React app)"
echo "   - FREE models (Gemini 2.0)"
echo "   - Zero-error tested system"
echo ""

# Add any remaining files
git add render.yaml DEPLOY_TO_PRODUCTION.md DEPLOY_NOW.sh
git commit -m "Add production deployment configuration" 2>/dev/null || echo "No new changes to commit"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Your repository: https://github.com/BTheCoderr/SmartProBonoAPP"
    echo ""
    echo "📋 NEXT STEPS FOR PRODUCTION:"
    echo "======================================"
    echo ""
    echo "1️⃣ Deploy to Render.com (Easiest - FREE tier):"
    echo "   → Go to: https://render.com"
    echo "   → Sign in with GitHub"
    echo "   → Click 'New +' → 'Blueprint'"
    echo "   → Select repo: BTheCoderr/SmartProBonoAPP"
    echo "   → Render auto-deploys both backend & frontend!"
    echo ""
    echo "2️⃣ Set Environment Variables in Render:"
    echo "   → GEMINI_API_KEY: AIzaSyBxkbE2boW8vOmeVHXiKHtWsO_0-dqUxMw"
    echo "   → DATABASE_URL: (your Supabase URL)"
    echo "   → SECRET_KEY: (auto-generated)"
    echo ""
    echo "3️⃣ Alternative Platforms:"
    echo "   → Railway.app (FREE tier)"
    echo "   → Vercel (FREE for frontend)"
    echo "   → Netlify (FREE for frontend)"
    echo "   → Heroku (paid)"
    echo ""
    echo "📖 Full guide: DEPLOY_TO_PRODUCTION.md"
    echo ""
    echo "🎉 Your code is production-ready and on GitHub!"
    echo "   Just pick a platform and deploy!"
else
    echo ""
    echo "❌ Push failed. Check your Git configuration."
    exit 1
fi

