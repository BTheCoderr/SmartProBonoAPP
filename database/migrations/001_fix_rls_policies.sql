-- Migration: Fix RLS Policy Performance Issues
-- Issue: auth_rls_initplan - auth.<function>() being re-evaluated for each row
-- Solution: Wrap auth functions in SELECT subquery to evaluate once per query
-- Date: 2025-10-08

-- ============================================================================
-- CASE_INTAKES TABLE - Fix RLS Policies
-- ============================================================================

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view own case intakes" ON public.case_intakes;
DROP POLICY IF EXISTS "Users can create case intakes" ON public.case_intakes;
DROP POLICY IF EXISTS "Users can update own case intakes" ON public.case_intakes;
DROP POLICY IF EXISTS "Service role can manage all case intakes" ON public.case_intakes;

-- Recreate with optimized auth function calls
CREATE POLICY "Users can view own case intakes" ON public.case_intakes
    FOR SELECT
    USING (user_id = (SELECT auth.uid()));

CREATE POLICY "Users can create case intakes" ON public.case_intakes
    FOR INSERT
    WITH CHECK (user_id = (SELECT auth.uid()));

CREATE POLICY "Users can update own case intakes" ON public.case_intakes
    FOR UPDATE
    USING (user_id = (SELECT auth.uid()));

CREATE POLICY "Service role can manage all case intakes" ON public.case_intakes
    FOR ALL
    USING ((SELECT auth.role()) = 'service_role');

-- ============================================================================
-- HUMAN_REVIEWS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Service role can manage human reviews" ON public.human_reviews;

CREATE POLICY "Service role can manage human reviews" ON public.human_reviews
    FOR ALL
    USING ((SELECT auth.role()) = 'service_role');

-- ============================================================================
-- LANGGRAPH_CHECKPOINTS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Service role can manage checkpoints" ON public.langgraph_checkpoints;

CREATE POLICY "Service role can manage checkpoints" ON public.langgraph_checkpoints
    FOR ALL
    USING ((SELECT auth.role()) = 'service_role');

-- ============================================================================
-- LAWYER_PROFILES TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Service role can manage lawyer profiles" ON public.lawyer_profiles;

CREATE POLICY "Service role can manage lawyer profiles" ON public.lawyer_profiles
    FOR ALL
    USING ((SELECT auth.role()) = 'service_role');

-- ============================================================================
-- AUDIT_LOGS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Admins can view all audit logs" ON public.audit_logs;

-- Create function to check if user is admin (cached per query)
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM public.users
        WHERE id = auth.uid()
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

CREATE POLICY "Admins can view all audit logs" ON public.audit_logs
    FOR SELECT
    USING ((SELECT public.is_admin()));

-- ============================================================================
-- USER_ACTIVITIES TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Users can view their own activities" ON public.user_activities;

CREATE POLICY "Users can view their own activities" ON public.user_activities
    FOR SELECT
    USING (user_id = (SELECT auth.uid()));

-- ============================================================================
-- SECURITY_EVENTS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Admins can view all security events" ON public.security_events;

CREATE POLICY "Admins can view all security events" ON public.security_events
    FOR SELECT
    USING ((SELECT public.is_admin()));

-- ============================================================================
-- PERFORMANCE_METRICS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Admins can view all performance metrics" ON public.performance_metrics;

CREATE POLICY "Admins can view all performance metrics" ON public.performance_metrics
    FOR SELECT
    USING ((SELECT public.is_admin()));

-- ============================================================================
-- COMPLIANCE_RECORDS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Users can view their own compliance records" ON public.compliance_records;
DROP POLICY IF EXISTS "Admins can view all compliance records" ON public.compliance_records;

CREATE POLICY "Users can view their own compliance records" ON public.compliance_records
    FOR SELECT
    USING (user_id = (SELECT auth.uid()));

CREATE POLICY "Admins can view all compliance records" ON public.compliance_records
    FOR SELECT
    USING ((SELECT public.is_admin()));

-- ============================================================================
-- API_AUDITS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Admins can view all API audits" ON public.api_audits;

CREATE POLICY "Admins can view all API audits" ON public.api_audits
    FOR SELECT
    USING ((SELECT public.is_admin()));

-- ============================================================================
-- DOCUMENT_AUDITS TABLE - Fix RLS Policies
-- ============================================================================

DROP POLICY IF EXISTS "Users can view their own document audits" ON public.document_audits;
DROP POLICY IF EXISTS "Admins can view all document audits" ON public.document_audits;

CREATE POLICY "Users can view their own document audits" ON public.document_audits
    FOR SELECT
    USING (user_id = (SELECT auth.uid()));

CREATE POLICY "Admins can view all document audits" ON public.document_audits
    FOR SELECT
    USING ((SELECT public.is_admin()));

-- Add comment to track migration
COMMENT ON FUNCTION public.is_admin() IS 'Optimized admin check function - Migration 001 - 2025-10-08';

