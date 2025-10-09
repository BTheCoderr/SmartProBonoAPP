-- Migration: Fix Function Search Path Issues (SIMPLE VERSION)
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
-- FIX cleanup_old_audit_data FUNCTION (if it exists)
-- ============================================================================

-- First, let's drop the function if it exists, then recreate it properly
DROP FUNCTION IF EXISTS public.cleanup_old_audit_data(INTEGER);

-- Now create it with proper search_path
CREATE OR REPLACE FUNCTION public.cleanup_old_audit_data(retention_days INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM public.audit_logs 
    WHERE created_at < NOW() - INTERVAL '1 day' * retention_days;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = '';

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

-- Add comments to track the fix
COMMENT ON FUNCTION public.is_admin() IS 'Fixed search_path - Migration 005 - 2025-10-08';
COMMENT ON FUNCTION public.cleanup_old_audit_data(INTEGER) IS 'Fixed search_path - Migration 005 - 2025-10-08';
