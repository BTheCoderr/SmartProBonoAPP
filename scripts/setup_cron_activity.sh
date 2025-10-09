#!/bin/bash
# Setup cron job to keep Supabase project active
# This prevents automatic pausing due to inactivity

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
KEEP_ACTIVE_SCRIPT="$SCRIPT_DIR/keep_project_active.py"
PYTHON_PATH=$(which python3)

echo "🔧 Setting up automated project activity monitor..."
echo "Project Directory: $PROJECT_DIR"
echo "Python Path: $PYTHON_PATH"

# Make the script executable
chmod +x "$KEEP_ACTIVE_SCRIPT"

# Create a cron job that runs every 12 hours
CRON_JOB="0 */12 * * * cd $PROJECT_DIR && $PYTHON_PATH $KEEP_ACTIVE_SCRIPT --once >> $PROJECT_DIR/project_activity.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "keep_project_active.py"; then
    echo "⚠️  Cron job already exists, updating..."
    (crontab -l 2>/dev/null | grep -v "keep_project_active.py"; echo "$CRON_JOB") | crontab -
else
    echo "➕ Adding new cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo "✅ Cron job installed successfully!"
echo ""
echo "📋 Cron Schedule:"
echo "   - Runs every 12 hours"
echo "   - Logs to: $PROJECT_DIR/project_activity.log"
echo ""
echo "🔍 To view current cron jobs:"
echo "   crontab -l"
echo ""
echo "📝 To view activity log:"
echo "   tail -f $PROJECT_DIR/project_activity.log"
echo ""
echo "⚠️  To remove the cron job:"
echo "   crontab -e"
echo "   (then delete the line with 'keep_project_active.py')"
echo ""
echo "🎯 Alternative: Run as background service"
echo "   python3 $KEEP_ACTIVE_SCRIPT &"
echo ""

# Run initial check
echo "🚀 Running initial health check..."
$PYTHON_PATH "$KEEP_ACTIVE_SCRIPT" --once

echo ""
echo "✅ Setup complete! Your Supabase project will stay active."

