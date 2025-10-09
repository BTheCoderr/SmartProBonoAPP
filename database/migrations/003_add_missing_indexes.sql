-- Migration: Add Missing Foreign Key Indexes
-- Issue: Foreign keys without covering indexes impact query performance
-- Solution: Add indexes on foreign key columns
-- Date: 2025-10-08

-- ============================================================================
-- COMPLIANCE_RECORDS TABLE
-- ============================================================================

-- Add index for processed_by foreign key
CREATE INDEX IF NOT EXISTS idx_compliance_records_processed_by 
    ON public.compliance_records(processed_by);

-- Add composite index for common queries
CREATE INDEX IF NOT EXISTS idx_compliance_records_user_status 
    ON public.compliance_records(user_id, status)
    WHERE status != 'completed';

-- ============================================================================
-- PERFORMANCE_METRICS TABLE
-- ============================================================================

-- Add index for user_id foreign key
CREATE INDEX IF NOT EXISTS idx_performance_metrics_user_id 
    ON public.performance_metrics(user_id);

-- Add composite index for common time-series queries
CREATE INDEX IF NOT EXISTS idx_performance_metrics_created_metric 
    ON public.performance_metrics(created_at DESC, metric_type);

-- ============================================================================
-- ADDITIONAL PERFORMANCE INDEXES
-- ============================================================================

-- Case intakes - optimize for common queries
CREATE INDEX IF NOT EXISTS idx_case_intakes_user_status_created 
    ON public.case_intakes(user_id, status, created_at DESC);

-- Audit logs - optimize for time-range queries
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_created_type 
    ON public.audit_logs(user_id, created_at DESC, event_type);

-- User activities - optimize for recent activity queries  
CREATE INDEX IF NOT EXISTS idx_user_activities_user_created_type 
    ON public.user_activities(user_id, created_at DESC, activity_type);

-- Security events - optimize for security monitoring
CREATE INDEX IF NOT EXISTS idx_security_events_severity_created 
    ON public.security_events(severity, created_at DESC)
    WHERE severity IN ('high', 'critical');

-- Document audits - optimize for audit trail queries
CREATE INDEX IF NOT EXISTS idx_document_audits_doc_created_action 
    ON public.document_audits(document_id, created_at DESC, action);

-- API audits - optimize for endpoint monitoring
CREATE INDEX IF NOT EXISTS idx_api_audits_endpoint_created 
    ON public.api_audits(endpoint, created_at DESC);

-- ============================================================================
-- ANALYZE TABLES
-- ============================================================================

-- Update table statistics after adding indexes
ANALYZE public.compliance_records;
ANALYZE public.performance_metrics;
ANALYZE public.case_intakes;
ANALYZE public.audit_logs;
ANALYZE public.user_activities;
ANALYZE public.security_events;
ANALYZE public.document_audits;
ANALYZE public.api_audits;

-- Add comment
COMMENT ON INDEX idx_compliance_records_processed_by IS 'Foreign key index - Migration 003 - 2025-10-08';
COMMENT ON INDEX idx_performance_metrics_user_id IS 'Foreign key index - Migration 003 - 2025-10-08';

