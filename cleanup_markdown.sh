#!/bin/bash
# Clean up redundant markdown files

echo "🧹 Cleaning up redundant markdown files..."
echo ""

# Files to KEEP (essential)
KEEP=(
  "README.md"
  "CONTRIBUTING.md"
  "SECURITY.md"
  "SETUP_GROQ.md"
  "DEPLOYMENT_READY.md"
  "FIXES_APPLIED.md"
  "QUICK_FIXES_SUMMARY.md"
)

# Files to DELETE (redundant/old)
DELETE=(
  # Old fix/solution files
  "ACTION_PLAN.md"
  "AI_CHAT_IMPROVEMENTS.md"
  "CHAT_FIX_SOLUTION.md"
  "FIXES_AND_NEXT_STEPS.md"
  "FIX_AI_TOOLS.md"
  "FIX_BLANK_PAGES.md"
  "QUICK_CHAT_FIX.md"
  "QUICK_FIX_FRONTEND.md"
  "QUICK_FIX_README.md"
  "QUICK_FIX_SUMMARY.md"
  
  # Old status/summary files
  "COMPLETE_SUCCESS_SUMMARY.md"
  "FINAL_COMPLETE_SYSTEM.md"
  "FINAL_SOLUTION_SUMMARY.md"
  "FINAL_STATUS_AND_SOLUTION.md"
  "FINAL_STATUS_REPORT.md"
  "FINAL_SUMMARY.md"
  "SUCCESS_SUMMARY.md"
  "WORKING_FEATURES_SUMMARY.md"
  
  # Old deployment guides
  "DEPLOYMENT_FIX.md"
  "DEPLOYMENT_FIX_V2.md"
  "DEPLOYMENT_GUIDE.md"
  "DEPLOY_TO_PRODUCTION.md"
  "RENDER_DEPLOYMENT_FIX.md"
  
  # Old setup guides
  "START_HERE.md"
  "START_HERE_AI_FIXED.md"
  "START_HERE_FRESH.md"
  "READ_THIS_FIRST.md"
  "QUICK_START.md"
  "QUICK_START_ENV.md"
  "QUICK_START_FIXED.md"
  "ENV_SETUP_GUIDE.md"
  "ENV_SETUP_COMPLETE.md"
  
  # Old test reports
  "APPLICATION_TEST_RESULTS.md"
  "FULL_APPLICATION_TEST_REPORT.md"
  "TEST_COMPLETE_SUMMARY.md"
  "TEST_SETUP_SOLUTION.md"
  
  # Old integration guides
  "AI_DEVELOPMENT_SETUP.md"
  "AI_TOOLS_README.md"
  "AI_TOOLS_STATUS.md"
  "COURTLISTENER_INTEGRATION.md"
  "LEGAL_AI_INTEGRATION.md"
  "SAUL_COMPLETE_GUIDE.md"
  "SAUL_FINAL_SUMMARY.md"
  "SAUL_INTEGRATION_GUIDE.md"
  "SMARTPROBONO_AGENT_INTEGRATION_GUIDE.md"
  
  # Old feature docs
  "ALL_65_PAGES.md"
  "DATABASE_OPTIMIZATION_GUIDE.md"
  "FREE_GEMINI_SETUP.md"
  "FRONTEND_DESIGN_FIXES.md"
  "IMPLEMENTATION_SUMMARY.md"
  "LIVEKIT_VOICE_AGENT_GUIDE.md"
  "MULTI_AGENT_SUCCESS.md"
  "NAVIGATION_GUIDE.md"
  "PERFORMANCE_FIXED.md"
  "PLATFORM_OVERVIEW.md"
  "PRODUCTION_READY_CHECKLIST.md"
  "ROUTE_OVERVIEW.md"
  "ROUTE_STATUS_REPORT.md"
  "VSCODE_SETUP.md"
  "YOUR_COMPLETE_AI_SYSTEM.md"
  "FIND_RENDER_ACCOUNT.md"
)

# Count before
BEFORE=$(find . -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')

# Delete redundant files
DELETED=0
for file in "${DELETE[@]}"; do
  if [ -f "$file" ]; then
    rm "$file"
    echo "❌ Deleted: $file"
    ((DELETED++))
  fi
done

# Count after
AFTER=$(find . -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')

echo ""
echo "📊 Summary:"
echo "   Before: $BEFORE files"
echo "   Deleted: $DELETED files"
echo "   After: $AFTER files"
echo ""
echo "✅ Cleanup complete!"
