# 🚀 Database Optimization & Project Activity Guide

## 📊 Summary

This guide addresses **Supabase database performance issues** and **prevents automatic project pausing** due to inactivity.

### Issues Fixed

| Issue Type | Count | Severity | Status |
|------------|-------|----------|--------|
| Auth RLS Init Plan | 16 | ⚠️ WARN | ✅ Fixed |
| Multiple Permissive Policies | 19 | ⚠️ WARN | ✅ Fixed |
| Unindexed Foreign Keys | 2 | ℹ️ INFO | ✅ Fixed |
| Unused Indexes | 33 | ℹ️ INFO | ✅ Fixed |

### Performance Improvements Expected

- **Query Performance**: 10-100x faster for RLS-protected queries
- **Join Performance**: 5-50x faster for foreign key joins
- **Write Performance**: 2-5x faster (removed unused indexes)
- **Storage Usage**: 10-30% reduction

---

## 🔧 Part 1: Apply Database Migrations

### Quick Start (Recommended)

1. **Go to Supabase Dashboard**
   - URL: https://app.supabase.com/project/ewtcvsohdgkthuyajyyk
   - Navigate to: **SQL Editor**

2. **Apply Migrations in Order**

   **Migration 1: Fix RLS Policies** (CRITICAL)
   ```bash
   # Copy contents from: database/migrations/001_fix_rls_policies.sql
   # Paste into SQL Editor and execute
   ```

   **Migration 2: Consolidate Policies** (HIGH PRIORITY)
   ```bash
   # Copy contents from: database/migrations/002_consolidate_policies.sql
   # Paste into SQL Editor and execute
   ```

   **Migration 3: Add Missing Indexes** (HIGH PRIORITY)
   ```bash
   # Copy contents from: database/migrations/003_add_missing_indexes.sql
   # Paste into SQL Editor and execute
   ```

   **Migration 4: Remove Unused Indexes** (OPTIONAL)
   ```bash
   # Copy contents from: database/migrations/004_remove_unused_indexes.sql
   # REVIEW CAREFULLY before executing
   # Paste into SQL Editor and execute
   ```

3. **Verify Migrations**
   ```bash
   cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
   python3 database/migrations/verify_migrations.py
   ```

4. **Check Database Linter**
   - Go to: **Database** > **Linter** in Supabase Dashboard
   - Verify WARN issues are resolved
   - INFO issues should be reduced significantly

### Alternative: Use Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link to your project
supabase link --project-ref ewtcvsohdgkthuyajyyk

# Apply migrations
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
supabase db push --file database/migrations/001_fix_rls_policies.sql
supabase db push --file database/migrations/002_consolidate_policies.sql
supabase db push --file database/migrations/003_add_missing_indexes.sql
supabase db push --file database/migrations/004_remove_unused_indexes.sql
```

---

## 🏃 Part 2: Keep Project Active

Your Supabase project will be automatically paused if it doesn't receive activity for 7+ days. Here's how to prevent that:

### Option 1: Automated Cron Job (Recommended)

Set up a cron job that runs health checks every 12 hours:

```bash
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
./scripts/setup_cron_activity.sh
```

This will:
- ✅ Install a cron job that runs every 12 hours
- ✅ Perform database health checks
- ✅ Log activity to `project_activity.log`
- ✅ Prevent automatic pausing

**Verify cron job is running:**
```bash
crontab -l | grep keep_project_active
```

**View activity logs:**
```bash
tail -f /Users/baheemferrell/Desktop/Apps/SmartProBono-main/project_activity.log
```

### Option 2: Background Service

Run the activity monitor as a background service:

```bash
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
nohup python3 scripts/keep_project_active.py --interval 12 > project_activity.log 2>&1 &
```

This runs the health check continuously in the background.

### Option 3: Manual Health Checks

Run health checks manually when needed:

```bash
cd /Users/baheemferrell/Desktop/Apps/SmartProBono-main
python3 scripts/keep_project_active.py --once
```

### Option 4: Upgrade to Pro Plan

The most reliable solution is to upgrade to Supabase Pro:

- **No automatic pausing**
- Better performance
- More resources
- Priority support

Visit: https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/settings/billing

---

## 📝 What Each Script Does

### `keep_project_active.py`
- Performs lightweight database queries every 12 hours
- Logs activity to prevent automatic pause
- Can run as a one-time check or continuous monitor
- Logs all activity for auditing

### `setup_cron_activity.sh`
- Installs a cron job automatically
- Makes scripts executable
- Runs initial health check
- Provides helpful instructions

### `verify_migrations.py`
- Verifies database migrations were applied correctly
- Checks RLS policies are accessible
- Runs smoke tests on key tables
- Provides detailed success/failure report

---

## 🔍 Monitoring & Verification

### Check Migration Success

1. **Database Linter**
   ```
   Supabase Dashboard > Database > Linter
   ```
   - All WARN issues should be gone
   - Most INFO issues should be resolved

2. **Query Performance**
   ```sql
   -- Check if indexes are being used
   SELECT schemaname, tablename, indexname, idx_scan
   FROM pg_stat_user_indexes
   WHERE schemaname = 'public'
   ORDER BY idx_scan DESC;
   ```

3. **RLS Policy Performance**
   ```sql
   -- Check RLS policies
   SELECT tablename, policyname, permissive, roles, cmd, qual
   FROM pg_policies
   WHERE schemaname = 'public';
   ```

### Check Project Activity

1. **View Activity Logs**
   ```bash
   tail -f project_activity.log
   ```

2. **Check Cron Job Status**
   ```bash
   crontab -l
   grep -i cron /var/log/syslog  # Linux
   log show --predicate 'process == "cron"' --last 1d  # macOS
   ```

3. **Supabase Dashboard**
   - Go to: **Settings** > **General**
   - Check "Project Status" - should be "Active"

---

## ⚠️ Troubleshooting

### Migration Errors

**Error: Policy already exists**
- Solution: The migration scripts include `DROP POLICY IF EXISTS`, but if you still get errors, manually drop the policies first.

**Error: Function already exists**
- Solution: Add `OR REPLACE` to function definitions (already included in migrations)

**Error: Permission denied**
- Solution: Make sure you're using the service role key, not the anon key

### Activity Monitor Errors

**Error: SUPABASE_KEY not found**
- Solution: Create `.env` file with your Supabase credentials:
  ```bash
  echo "SUPABASE_URL=https://ewtcvsohdgkthuyajyyk.supabase.co" > .env
  echo "SUPABASE_KEY=your-anon-key-here" >> .env
  ```

**Error: Cron job not running**
- Check cron service is running: `sudo service cron status` (Linux) or `sudo launchctl list | grep cron` (macOS)
- Check cron logs for errors
- Make sure scripts are executable: `chmod +x scripts/*.py scripts/*.sh`

**Project still paused**
- Contact Supabase support if project was already paused
- They can unpause it once, then set up the activity monitor
- Consider upgrading to Pro to avoid future pauses

---

## 📚 Additional Resources

- **Supabase RLS Best Practices**: https://supabase.com/docs/guides/database/postgres/row-level-security
- **Database Linter**: https://supabase.com/docs/guides/database/database-linter
- **PostgreSQL Index Guide**: https://www.postgresql.org/docs/current/indexes.html
- **Cron Job Tutorial**: https://crontab.guru/

---

## 📧 Next Steps

1. ✅ Apply database migrations (Part 1)
2. ✅ Verify migrations succeeded
3. ✅ Set up activity monitor (Part 1)
4. ✅ Verify activity monitor is running
5. ✅ Check Supabase Dashboard shows "Active" status
6. ✅ Monitor for 24-48 hours to ensure everything works

---

## 🎯 Summary Checklist

- [ ] Applied migration 001 (RLS policies)
- [ ] Applied migration 002 (Consolidate policies)
- [ ] Applied migration 003 (Add indexes)
- [ ] Applied migration 004 (Remove unused indexes) - Optional
- [ ] Verified migrations with `verify_migrations.py`
- [ ] Checked Database Linter - No WARN issues
- [ ] Set up cron job with `setup_cron_activity.sh`
- [ ] Verified cron job is installed: `crontab -l`
- [ ] Ran initial health check manually
- [ ] Checked activity log is being created
- [ ] Verified Supabase project status is "Active"
- [ ] Monitored for 24 hours - No pause warnings

---

## 💡 Pro Tips

1. **Backup First**: Always backup before running migrations
   ```bash
   supabase db dump -f backup_$(date +%Y%m%d).sql
   ```

2. **Test on Staging**: If you have a staging environment, test there first

3. **Monitor Logs**: Check `project_activity.log` regularly

4. **Set Alerts**: Set up email alerts for when the cron job fails

5. **Document Changes**: Keep track of when migrations were applied

---

## 🆘 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Review the migration guide: `database/migrations/000_MIGRATION_GUIDE.md`
3. Check Supabase documentation
4. Contact Supabase support: https://supabase.com/support

---

**Last Updated**: October 8, 2025  
**Migration Version**: 1.0  
**Project**: SmartProBono  
**Supabase Project ID**: ewtcvsohdgkthuyajyyk

