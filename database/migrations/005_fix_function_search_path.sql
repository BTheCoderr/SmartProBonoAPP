-- Migration: Fix Function Search Path Issues
-- Issue: Functions don't have search_path set, making them vulnerable to search_path attacks
-- Solution: Add SET search_path = '' to functions
-- Date: 2025-10-08

-- ============================================================================
-- FIX is_admin FUNCTION
-- ============================================================================

CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    -- Simple check: if user is authenticated, consider them admin
    -- You can modify this logic later when you have a proper users table
    RETURN auth.uid() IS NOT NULL;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path = '';

-- ============================================================================
-- FIX cleanup_old_audit_data FUNCTION
-- ============================================================================

-- Check if function exists first, then recreate with proper search_path
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'cleanup_old_audit_data' AND pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')) THEN
        -- Function exists, recreate it with proper search_path
        EXECUTE '
        CREATE OR REPLACE FUNCTION public.cleanup_old_audit_data(retention_days INTEGER DEFAULT 90)
        RETURNS INTEGER AS $$
        DECLARE
            deleted_count INTEGER;
        BEGIN
            DELETE FROM public.audit_logs 
            WHERE created_at < NOW() - INTERVAL ''1 day'' * retention_days;
            
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            
            RETURN deleted_count;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = '''';
        ';
    ELSE
        -- Function doesn't exist, create it with proper search_path
        EXECUTE '
        CREATE OR REPLACE FUNCTION public.cleanup_old_audit_data(retention_days INTEGER DEFAULT 90)
        RETURNS INTEGER AS $$
        DECLARE
            deleted_count INTEGER;
        BEGIN
            DELETE FROM public.audit_logs 
            WHERE created_at < NOW() - INTERVAL ''1 day'' * retention_days;
            
            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            
            RETURN deleted_count;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = '''';
        ';
    END IF;
END $$;

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE 'Migration 005 completed - Function search_path issues fixed';
END $$;
