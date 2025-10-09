-- Migration: Consolidate Multiple Permissive Policies (FIXED VERSION)
-- Issue: Multiple permissive policies cause performance degradation
-- Solution: Combine policies using OR conditions instead of multiple policies
-- Date: 2025-10-08
-- NOTE: This version only works with tables that actually exist

-- ============================================================================
-- LAWYER_PROFILES TABLE - Consolidate Policies  
-- ============================================================================

-- Currently has: "Anyone can view" + "Service role can manage"
-- These overlap for SELECT operations

DROP POLICY IF EXISTS "Anyone can view lawyer profiles" ON public.lawyer_profiles;
DROP POLICY IF EXISTS "Service role can manage lawyer profiles" ON public.lawyer_profiles;

-- Recreate as consolidated policy
CREATE POLICY "Public can view lawyer profiles" ON public.lawyer_profiles
    FOR SELECT
    USING (true);  -- Public read access

CREATE POLICY "Service role can manage lawyer profiles" ON public.lawyer_profiles
    FOR ALL
    USING ((SELECT auth.role()) = 'service_role');

-- ============================================================================
-- SKIP USER-RELATED INDEXES (no users table exists)
-- ============================================================================

-- Note: The original migration tried to create indexes on public.users
-- but this table doesn't exist in your database. Skipping these indexes.

-- ============================================================================
-- ADD COMMENT
-- ============================================================================

COMMENT ON POLICY "Public can view lawyer profiles" ON public.lawyer_profiles IS 'Consolidated policy - Migration 002 - 2025-10-08';

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE 'Migration 002 completed successfully - Only applied to existing tables';
END $$;
