#!/bin/bash
# Quick Fix Database - One-command solution for database optimization
# This script helps apply migrations and set up activity monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MIGRATION_DIR="$PROJECT_DIR/database/migrations"

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}    SmartProBono Database Optimization & Activity Setup    ${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

print_success "Python 3 found"

# Check if migrations directory exists
if [ ! -d "$MIGRATION_DIR" ]; then
    print_error "Migration directory not found: $MIGRATION_DIR"
    exit 1
fi

print_success "Migration files found"

# Main menu
echo ""
echo "What would you like to do?"
echo ""
echo "1) View migration files (to apply manually in Supabase Dashboard)"
echo "2) Set up automated project activity monitor"
echo "3) Run manual health check"
echo "4) Verify migrations were applied"
echo "5) Show Supabase Dashboard URL"
echo "6) Do everything (setup activity monitor + show migration instructions)"
echo "7) Exit"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        print_info "Migration files location:"
        echo ""
        echo "📁 $MIGRATION_DIR"
        echo ""
        print_info "Apply these migrations in order:"
        echo ""
        echo "1. 001_fix_rls_policies.sql       (CRITICAL - Fix RLS performance)"
        echo "2. 002_consolidate_policies.sql   (HIGH - Consolidate policies)"
        echo "3. 003_add_missing_indexes.sql    (HIGH - Add indexes)"
        echo "4. 004_remove_unused_indexes.sql  (OPTIONAL - Clean up)"
        echo ""
        print_info "How to apply:"
        echo ""
        echo "1. Go to: https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/sql"
        echo "2. Click 'New Query'"
        echo "3. Copy contents of migration file"
        echo "4. Paste and click 'Run'"
        echo "5. Repeat for each migration"
        echo ""
        ls -1 "$MIGRATION_DIR"/*.sql 2>/dev/null || print_warning "No SQL files found"
        ;;
    
    2)
        echo ""
        print_info "Setting up automated activity monitor..."
        "$SCRIPT_DIR/setup_cron_activity.sh"
        print_success "Activity monitor setup complete!"
        ;;
    
    3)
        echo ""
        print_info "Running manual health check..."
        python3 "$SCRIPT_DIR/keep_project_active.py" --once
        ;;
    
    4)
        echo ""
        print_info "Verifying migrations..."
        python3 "$MIGRATION_DIR/verify_migrations.py"
        ;;
    
    5)
        echo ""
        print_info "Supabase Dashboard URLs:"
        echo ""
        echo "🔗 SQL Editor:"
        echo "   https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/sql"
        echo ""
        echo "🔗 Database Linter:"
        echo "   https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/database/linter"
        echo ""
        echo "🔗 Project Settings:"
        echo "   https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/settings"
        echo ""
        ;;
    
    6)
        echo ""
        print_info "Setting up complete solution..."
        echo ""
        
        # Step 1: Show migration instructions
        print_info "STEP 1: Apply Database Migrations"
        echo ""
        echo "📋 You need to apply these migrations in Supabase Dashboard:"
        echo ""
        echo "   https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/sql"
        echo ""
        echo "Migration files are located in:"
        echo "   $MIGRATION_DIR"
        echo ""
        echo "Apply in this order:"
        echo "   1. 001_fix_rls_policies.sql"
        echo "   2. 002_consolidate_policies.sql"
        echo "   3. 003_add_missing_indexes.sql"
        echo "   4. 004_remove_unused_indexes.sql (optional)"
        echo ""
        
        read -p "Press Enter after you've applied the migrations..."
        
        # Step 2: Set up activity monitor
        echo ""
        print_info "STEP 2: Setting up Activity Monitor"
        echo ""
        "$SCRIPT_DIR/setup_cron_activity.sh"
        
        # Step 3: Verify
        echo ""
        print_info "STEP 3: Verification"
        echo ""
        read -p "Would you like to verify migrations now? (y/n): " verify
        if [ "$verify" = "y" ] || [ "$verify" = "Y" ]; then
            python3 "$MIGRATION_DIR/verify_migrations.py"
        fi
        
        echo ""
        print_success "Complete setup finished!"
        echo ""
        print_info "Next steps:"
        echo "1. Check Database Linter for remaining issues"
        echo "2. Monitor activity log: tail -f $PROJECT_DIR/project_activity.log"
        echo "3. Verify cron job: crontab -l"
        ;;
    
    7)
        echo ""
        print_info "Exiting..."
        exit 0
        ;;
    
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_success "Done!"
echo ""
print_info "For more information, see:"
echo "   $PROJECT_DIR/DATABASE_OPTIMIZATION_GUIDE.md"
echo ""

