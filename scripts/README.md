# SmartProBono Utility Scripts

This directory contains utility scripts for database optimization and project maintenance.

## Scripts Overview

### 🚀 Quick Fix Database
**File**: `quick_fix_database.sh`

Interactive script to fix database performance and set up activity monitoring.

```bash
./scripts/quick_fix_database.sh
```

**Options:**
1. View migration files
2. Set up activity monitor
3. Run manual health check
4. Verify migrations
5. Show Supabase URLs
6. Do everything (recommended)

---

### 🏃 Keep Project Active
**File**: `keep_project_active.py`

Prevents Supabase project from auto-pausing due to inactivity.

```bash
# Run once
python3 scripts/keep_project_active.py --once

# Run continuously (every 12 hours)
python3 scripts/keep_project_active.py --interval 12

# Run in background
nohup python3 scripts/keep_project_active.py --interval 12 > project_activity.log 2>&1 &
```

**What it does:**
- Performs lightweight database queries
- Logs all activity
- Prevents automatic project pause
- Runs health checks

---

### ⚙️ Setup Cron Activity
**File**: `setup_cron_activity.sh`

Automatically installs a cron job to keep project active.

```bash
./scripts/setup_cron_activity.sh
```

**What it does:**
- Installs cron job (runs every 12 hours)
- Makes scripts executable
- Runs initial health check
- Provides verification instructions

**Verify installation:**
```bash
crontab -l | grep keep_project_active
```

**View logs:**
```bash
tail -f project_activity.log
```

---

## Common Tasks

### Fix Everything at Once
```bash
./scripts/quick_fix_database.sh
# Choose option 6
```

### Manual Health Check
```bash
python3 scripts/keep_project_active.py --once
```

### Set Up Automated Monitoring
```bash
./scripts/setup_cron_activity.sh
```

### Verify Migrations
```bash
python3 database/migrations/verify_migrations.py
```

### Check Cron Job Status
```bash
crontab -l
tail -f project_activity.log
```

---

## Troubleshooting

### Scripts Not Executable
```bash
chmod +x scripts/*.sh scripts/*.py
```

### Python Not Found
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Check version
python3 --version
```

### Cron Job Not Running
```bash
# Check cron service
sudo service cron status  # Linux
sudo launchctl list | grep cron  # macOS

# View cron logs
grep CRON /var/log/syslog  # Linux
log show --predicate 'process == "cron"' --last 1d  # macOS
```

### Activity Monitor Not Working
```bash
# Check environment variables
cat .env

# Run with debug output
python3 scripts/keep_project_active.py --once --debug
```

---

## Additional Scripts

### Other Utility Scripts in Project

- `seed_harvard_cases.py` - Seed legal case data
- `setup_embedded_search.py` - Setup vector search
- `setup_legal_ai.sh` - Setup legal AI backend

See respective README files for more information.

---

## Requirements

- Python 3.7+
- Supabase account with valid credentials
- Unix-like system (macOS, Linux, WSL on Windows)

---

## Environment Variables

Create `.env` file in project root:

```bash
SUPABASE_URL=https://ewtcvsohdgkthuyajyyk.supabase.co
SUPABASE_KEY=your-anon-key-here
# or
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

---

## Need Help?

- **Quick Fix Guide**: `/QUICK_FIX_README.md`
- **Comprehensive Guide**: `/DATABASE_OPTIMIZATION_GUIDE.md`
- **Migration Details**: `/database/migrations/000_MIGRATION_GUIDE.md`
- **Supabase Support**: https://supabase.com/support

---

**Last Updated**: October 8, 2025

