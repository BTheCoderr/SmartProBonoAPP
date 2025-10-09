# Database Performance Migrations Guide

## Overview

This directory contains SQL migrations to fix Supabase database linter warnings and improve performance.

## Issues Fixed

### 1. **Auth RLS Initialization Plan (WARN)**
- **Problem**: `auth.<function>()` calls being re-evaluated for each row
- **Impact**: Poor query performance at scale
- **Solution**: Wrap auth functions in SELECT subquery `(SELECT auth.uid())`

### 2. **Multiple Permissive Policies (WARN)**
- **Problem**: Multiple permissive policies for same role/action
- **Impact**: Each policy evaluated for every query
- **Solution**: Consolidate policies using OR conditions

### 3. **Unindexed Foreign Keys (INFO)**
- **Problem**: Foreign keys without covering indexes
- **Impact**: Slow joins and lookups
- **Solution**: Add indexes on foreign key columns

### 4. **Unused Indexes (INFO)**
- **Problem**: Indexes that are never used
- **Impact**: Wasted storage, slower writes
- **Solution**: Remove unused indexes, replace with composite indexes

## Migration Files

| File | Description | Impact |
|------|-------------|--------|
| `001_fix_rls_policies.sql` | Optimize RLS policy performance | ⚡ High - Fixes critical performance issue |
| `002_consolidate_policies.sql` | Consolidate overlapping policies | ⚡ Medium - Reduces policy evaluation overhead |
| `003_add_missing_indexes.sql` | Add foreign key and composite indexes | ⚡ High - Improves query performance |
| `004_remove_unused_indexes.sql` | Remove unused indexes | ⚡ Low - Reduces storage, faster writes |

## How to Apply Migrations

### Option 1: Supabase Dashboard (Recommended)

1. Go to your Supabase Dashboard: https://app.supabase.com
2. Select your project: `Smartprobono.org's Project`
3. Navigate to **SQL Editor**
4. Create a new query
5. Copy and paste the contents of each migration file in order
6. Execute each migration

**Order of execution:**
```
001_fix_rls_policies.sql
002_consolidate_policies.sql  
003_add_missing_indexes.sql
004_remove_unused_indexes.sql (Optional - review first)
```

### Option 2: Supabase CLI

```bash
# Install Supabase CLI if not already installed
npm install -g supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref ewtcvsohdgkthuyajyyk

# Run migrations
supabase db push --file database/migrations/001_fix_rls_policies.sql
supabase db push --file database/migrations/002_consolidate_policies.sql
supabase db push --file database/migrations/003_add_missing_indexes.sql
supabase db push --file database/migrations/004_remove_unused_indexes.sql
```

### Option 3: Direct PostgreSQL Connection

```bash
# Using psql
psql "postgresql://postgres:[YOUR-PASSWORD]@db.ewtcvsohdgkthuyajyyk.supabase.co:5432/postgres" \
  -f database/migrations/001_fix_rls_policies.sql
```

## Testing After Migration

After applying migrations, run the verification script:

```bash
python database/migrations/verify_migrations.py
```

Or manually check:

1. **Database Linter**: Check Supabase Dashboard > Database > Linter
   - All WARN issues should be resolved
   - INFO issues should be reduced

2. **Query Performance**: Run test queries to verify improvement

3. **RLS Policies**: Test authentication flows to ensure policies work correctly

## Rollback Plan

Each migration includes DROP statements for policies/indexes before creating new ones. If you need to rollback:

1. **Backup First**: Always backup before migrations
   ```bash
   supabase db dump -f backup_$(date +%Y%m%d).sql
   ```

2. **Restore if needed**:
   ```bash
   supabase db push --file backup_20251008.sql
   ```

## Performance Improvements Expected

| Area | Before | After | Improvement |
|------|--------|-------|-------------|
| RLS Policy Evaluation | Per-row | Per-query | 10-100x faster |
| Foreign Key Joins | Seq Scan | Index Scan | 5-50x faster |
| Write Operations | Slow (unused indexes) | Fast | 2-5x faster |
| Storage Usage | High (unused indexes) | Reduced | 10-30% less |

## Tables Affected

- ✅ `case_intakes` - RLS optimized, indexes improved
- ✅ `human_reviews` - RLS optimized
- ✅ `langgraph_checkpoints` - RLS optimized
- ✅ `lawyer_profiles` - RLS optimized, policies consolidated
- ✅ `audit_logs` - RLS optimized, indexes improved
- ✅ `user_activities` - RLS optimized, indexes improved
- ✅ `security_events` - RLS optimized, indexes improved
- ✅ `performance_metrics` - RLS optimized, indexes improved
- ✅ `compliance_records` - RLS optimized, indexes improved
- ✅ `api_audits` - RLS optimized, indexes improved
- ✅ `document_audits` - RLS optimized, indexes improved

## Additional Optimizations

The migrations also create a helper function:

```sql
public.is_admin() -- Efficiently checks if user is admin
```

This function is used by multiple RLS policies and is marked as `STABLE SECURITY DEFINER` for optimal performance.

## Monitoring

After applying migrations, monitor:

1. **Query Performance**: Check slow query logs
2. **Index Usage**: Monitor `pg_stat_user_indexes`
3. **RLS Policy Performance**: Check query execution plans
4. **Database Size**: Should decrease after removing unused indexes

## Support

If you encounter issues:

1. Check Supabase Dashboard > Database > Linter for new warnings
2. Review PostgreSQL logs for errors
3. Test RLS policies with different user roles
4. Run `EXPLAIN ANALYZE` on slow queries

## References

- [Supabase RLS Performance Guide](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase Database Linter](https://supabase.com/docs/guides/database/database-linter)
- [PostgreSQL Index Performance](https://www.postgresql.org/docs/current/indexes.html)

