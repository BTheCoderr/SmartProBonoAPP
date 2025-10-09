-- Migration: Remove Unused Indexes
-- Issue: Unused indexes consume storage and slow down writes
-- Solution: Drop indexes that have never been used
-- Date: 2025-10-08
-- WARNING: This migration removes unused indexes. Review carefully before applying.

-- ============================================================================
-- CASE_INTAKES TABLE - Remove Redundant Indexes
-- ============================================================================

-- These indexes are being replaced by composite indexes in migration 003
-- Drop simple indexes that are covered by composite indexes

-- Keep: idx_case_intakes_user_status_created (composite - from migration 003)
-- Remove: idx_case_intakes_user_id (covered by composite)
-- Remove: idx_case_intakes_status (covered by composite)  
-- Remove: idx_case_intakes_created_at (covered by composite)

DROP INDEX IF EXISTS public.idx_case_intakes_user_id;
DROP INDEX IF EXISTS public.idx_case_intakes_status;
DROP INDEX IF EXISTS public.idx_case_intakes_created_at;

-- ============================================================================
-- AUDIT_LOGS TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_audit_logs_user_created_type (composite - from migration 003)
-- Remove: Simple indexes covered by composite

DROP INDEX IF EXISTS public.idx_audit_logs_user_id;
DROP INDEX IF EXISTS public.idx_audit_logs_event_type;
DROP INDEX IF EXISTS public.idx_audit_logs_created_at;
DROP INDEX IF EXISTS public.idx_audit_logs_severity;

-- ============================================================================
-- USER_ACTIVITIES TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_user_activities_user_created_type (composite - from migration 003)
-- Remove: Simple indexes covered by composite

DROP INDEX IF EXISTS public.idx_user_activities_user_id;
DROP INDEX IF EXISTS public.idx_user_activities_activity_type;
DROP INDEX IF EXISTS public.idx_user_activities_created_at;

-- ============================================================================
-- SECURITY_EVENTS TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_security_events_severity_created (partial - from migration 003)
-- Remove: Redundant simple indexes

DROP INDEX IF EXISTS public.idx_security_events_user_id;
DROP INDEX IF EXISTS public.idx_security_events_event_type;
DROP INDEX IF EXISTS public.idx_security_events_created_at;
DROP INDEX IF EXISTS public.idx_security_events_severity;

-- ============================================================================
-- PERFORMANCE_METRICS TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_performance_metrics_user_id (foreign key - from migration 003)
-- Keep: idx_performance_metrics_created_metric (composite - from migration 003)
-- Remove: Redundant simple indexes

DROP INDEX IF EXISTS public.idx_performance_metrics_metric_type;
DROP INDEX IF EXISTS public.idx_performance_metrics_created_at;
DROP INDEX IF EXISTS public.idx_performance_metrics_endpoint;

-- ============================================================================
-- COMPLIANCE_RECORDS TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_compliance_records_processed_by (foreign key - from migration 003)
-- Keep: idx_compliance_records_user_status (composite - from migration 003)
-- Remove: Redundant simple indexes

DROP INDEX IF EXISTS public.idx_compliance_records_user_id;
DROP INDEX IF EXISTS public.idx_compliance_records_record_type;
DROP INDEX IF EXISTS public.idx_compliance_records_status;
DROP INDEX IF EXISTS public.idx_compliance_records_created_at;

-- ============================================================================
-- API_AUDITS TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_api_audits_endpoint_created (composite - from migration 003)
-- Remove: Redundant simple indexes

DROP INDEX IF EXISTS public.idx_api_audits_endpoint;
DROP INDEX IF EXISTS public.idx_api_audits_user_id;
DROP INDEX IF EXISTS public.idx_api_audits_created_at;

-- ============================================================================
-- DOCUMENT_AUDITS TABLE - Remove Redundant Indexes
-- ============================================================================

-- Keep: idx_document_audits_doc_created_action (composite - from migration 003)
-- Remove: Redundant simple indexes

DROP INDEX IF EXISTS public.idx_document_audits_document_id;
DROP INDEX IF EXISTS public.idx_document_audits_user_id;
DROP INDEX IF EXISTS public.idx_document_audits_action;
DROP INDEX IF EXISTS public.idx_document_audits_created_at;

-- ============================================================================
-- HUMAN_REVIEWS TABLE - Remove Unused Indexes
-- ============================================================================

DROP INDEX IF EXISTS public.idx_human_reviews_thread_id;
DROP INDEX IF EXISTS public.idx_human_reviews_status;

-- ============================================================================
-- LANGGRAPH_CHECKPOINTS TABLE - Remove Unused Indexes
-- ============================================================================

DROP INDEX IF EXISTS public.idx_langgraph_checkpoints_thread_id;

-- ============================================================================
-- VACUUM TABLES
-- ============================================================================

-- Reclaim space from dropped indexes
VACUUM ANALYZE public.case_intakes;
VACUUM ANALYZE public.audit_logs;
VACUUM ANALYZE public.user_activities;
VACUUM ANALYZE public.security_events;
VACUUM ANALYZE public.performance_metrics;
VACUUM ANALYZE public.compliance_records;
VACUUM ANALYZE public.api_audits;
VACUUM ANALYZE public.document_audits;
VACUUM ANALYZE public.human_reviews;
VACUUM ANALYZE public.langgraph_checkpoints;

-- Log migration completion
DO $$
BEGIN
    RAISE NOTICE 'Migration 004 completed - Unused indexes removed - %', NOW();
END $$;

