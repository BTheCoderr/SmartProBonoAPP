-- Fixed Audit System Database Schema for SmartProBono
-- This schema works with Supabase's auth.users table structure

-- Create audit event types enum
CREATE TYPE audit_event_type AS ENUM (
    'security',
    'user_activity', 
    'data_access',
    'data_modification',
    'performance',
    'api_usage',
    'document_access',
    'compliance',
    'system'
);

-- Create audit severity enum
CREATE TYPE audit_severity AS ENUM (
    'low',
    'medium', 
    'high',
    'critical'
);

-- General system audit trail
CREATE TABLE audit_logs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type audit_event_type NOT NULL,
    severity audit_severity DEFAULT 'low',
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    session_id varchar(255),
    ip_address varchar(45), -- IPv6 support
    user_agent text,
    endpoint varchar(255),
    method varchar(10),
    status_code integer,
    request_data text, -- JSON string
    response_data text, -- JSON string
    error_message text,
    processing_time_ms integer,
    resource_id varchar(255), -- ID of affected resource
    resource_type varchar(100), -- Type of affected resource
    action varchar(100) NOT NULL, -- CREATE, READ, UPDATE, DELETE, etc.
    description text,
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- User interaction tracking
CREATE TABLE user_activities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    activity_type varchar(50) NOT NULL, -- page_view, click, form_submission, etc.
    page_url text,
    page_title varchar(255),
    referrer text,
    element_id varchar(255),
    element_class varchar(255),
    duration_seconds integer,
    device_type varchar(50),
    browser varchar(100),
    os varchar(100),
    screen_resolution varchar(20),
    action varchar(100),
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- Security events tracking
CREATE TABLE security_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type varchar(100) NOT NULL, -- failed_login, suspicious_activity, etc.
    severity audit_severity DEFAULT 'medium',
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    ip_address varchar(45),
    user_agent text,
    reason text,
    blocked boolean DEFAULT false,
    response_action varchar(100), -- block_ip, require_2fa, etc.
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- Performance metrics tracking
CREATE TABLE performance_metrics (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_type varchar(100) NOT NULL, -- response_time, cpu_usage, memory_usage, etc.
    value decimal(10,2) NOT NULL,
    unit varchar(20), -- ms, %, bytes, etc.
    threshold decimal(10,2),
    exceeded_threshold boolean DEFAULT false,
    endpoint varchar(255),
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- Compliance records tracking
CREATE TABLE compliance_records (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    record_type varchar(100) NOT NULL, -- gdpr_request, ccpa_request, consent_management, etc.
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    request_id varchar(255),
    status varchar(50) DEFAULT 'pending', -- pending, processing, completed, failed
    description text,
    data_subject varchar(255),
    data_types text[], -- Array of data types
    legal_basis varchar(100),
    retention_period integer, -- Days
    processed_by uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    processed_at timestamp,
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- API usage auditing
CREATE TABLE api_audits (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint varchar(255) NOT NULL,
    method varchar(10) NOT NULL,
    response_time_ms integer,
    status_code integer,
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    api_key_id varchar(255),
    request_size integer,
    response_size integer,
    rate_limit_hit boolean DEFAULT false,
    rate_limit_remaining integer,
    error_message text,
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- Document access auditing
CREATE TABLE document_audits (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid NOT NULL, -- References your documents table
    user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    action varchar(100) NOT NULL, -- view, download, edit, share, delete, etc.
    file_size integer,
    processing_time_ms integer,
    version varchar(50),
    shared_with uuid[], -- Array of user IDs
    changes_made text, -- JSON string of changes
    audit_metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- Create indexes for better performance
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_severity ON audit_logs(severity);

CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX idx_user_activities_activity_type ON user_activities(activity_type);
CREATE INDEX idx_user_activities_created_at ON user_activities(created_at);

CREATE INDEX idx_security_events_user_id ON security_events(user_id);
CREATE INDEX idx_security_events_event_type ON security_events(event_type);
CREATE INDEX idx_security_events_created_at ON security_events(created_at);
CREATE INDEX idx_security_events_severity ON security_events(severity);

CREATE INDEX idx_performance_metrics_metric_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_created_at ON performance_metrics(created_at);
CREATE INDEX idx_performance_metrics_endpoint ON performance_metrics(endpoint);

CREATE INDEX idx_compliance_records_user_id ON compliance_records(user_id);
CREATE INDEX idx_compliance_records_record_type ON compliance_records(record_type);
CREATE INDEX idx_compliance_records_status ON compliance_records(status);
CREATE INDEX idx_compliance_records_created_at ON compliance_records(created_at);

CREATE INDEX idx_api_audits_endpoint ON api_audits(endpoint);
CREATE INDEX idx_api_audits_user_id ON api_audits(user_id);
CREATE INDEX idx_api_audits_created_at ON api_audits(created_at);

CREATE INDEX idx_document_audits_document_id ON document_audits(document_id);
CREATE INDEX idx_document_audits_user_id ON document_audits(user_id);
CREATE INDEX idx_document_audits_action ON document_audits(action);
CREATE INDEX idx_document_audits_created_at ON document_audits(created_at);

-- Enable Row Level Security (RLS) for all audit tables
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_audits ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for audit_logs (Admin-only access)
CREATE POLICY "Admins can view all audit logs" ON audit_logs
  FOR SELECT TO authenticated USING (
    EXISTS (
      SELECT 1 FROM auth.users 
      WHERE auth.users.id = auth.uid() 
      AND auth.users.raw_user_meta_data->>'role' = 'admin'
    )
  );

CREATE POLICY "System can insert audit logs" ON audit_logs
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create RLS policies for user_activities
CREATE POLICY "Users can view their own activities" ON user_activities
  FOR SELECT TO authenticated USING (user_id = auth.uid());

CREATE POLICY "System can insert user activities" ON user_activities
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create RLS policies for security_events (Admin-only access)
CREATE POLICY "Admins can view all security events" ON security_events
  FOR SELECT TO authenticated USING (
    EXISTS (
      SELECT 1 FROM auth.users 
      WHERE auth.users.id = auth.uid() 
      AND auth.users.raw_user_meta_data->>'role' = 'admin'
    )
  );

CREATE POLICY "System can insert security events" ON security_events
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create RLS policies for performance_metrics (Admin-only access)
CREATE POLICY "Admins can view all performance metrics" ON performance_metrics
  FOR SELECT TO authenticated USING (
    EXISTS (
      SELECT 1 FROM auth.users 
      WHERE auth.users.id = auth.uid() 
      AND auth.users.raw_user_meta_data->>'role' = 'admin'
    )
  );

CREATE POLICY "System can insert performance metrics" ON performance_metrics
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create RLS policies for compliance_records
CREATE POLICY "Users can view their own compliance records" ON compliance_records
  FOR SELECT TO authenticated USING (user_id = auth.uid());

CREATE POLICY "Admins can view all compliance records" ON compliance_records
  FOR SELECT TO authenticated USING (
    EXISTS (
      SELECT 1 FROM auth.users 
      WHERE auth.users.id = auth.uid() 
      AND auth.users.raw_user_meta_data->>'role' = 'admin'
    )
  );

CREATE POLICY "System can insert compliance records" ON compliance_records
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create RLS policies for api_audits (Admin-only access)
CREATE POLICY "Admins can view all API audits" ON api_audits
  FOR SELECT TO authenticated USING (
    EXISTS (
      SELECT 1 FROM auth.users 
      WHERE auth.users.id = auth.uid() 
      AND auth.users.raw_user_meta_data->>'role' = 'admin'
    )
  );

CREATE POLICY "System can insert API audits" ON api_audits
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create RLS policies for document_audits
CREATE POLICY "Users can view their own document audits" ON document_audits
  FOR SELECT TO authenticated USING (user_id = auth.uid());

CREATE POLICY "Admins can view all document audits" ON document_audits
  FOR SELECT TO authenticated USING (
    EXISTS (
      SELECT 1 FROM auth.users 
      WHERE auth.users.id = auth.uid() 
      AND auth.users.raw_user_meta_data->>'role' = 'admin'
    )
  );

CREATE POLICY "System can insert document audits" ON document_audits
  FOR INSERT TO authenticated WITH CHECK (true);

-- Create cleanup function for old audit data
CREATE OR REPLACE FUNCTION cleanup_old_audit_data(retention_days integer DEFAULT 90)
RETURNS void AS $$
BEGIN
    -- Clean up old audit logs
    DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '1 day' * retention_days;
    
    -- Clean up old user activities
    DELETE FROM user_activities WHERE created_at < NOW() - INTERVAL '1 day' * retention_days;
    
    -- Clean up old security events (keep longer)
    DELETE FROM security_events WHERE created_at < NOW() - INTERVAL '1 day' * (retention_days * 4);
    
    -- Clean up old performance metrics (keep shorter)
    DELETE FROM performance_metrics WHERE created_at < NOW() - INTERVAL '1 day' * 30;
    
    -- Clean up old API audits
    DELETE FROM api_audits WHERE created_at < NOW() - INTERVAL '1 day' * retention_days;
    
    -- Clean up old document audits
    DELETE FROM document_audits WHERE created_at < NOW() - INTERVAL '1 day' * retention_days;
    
    -- Keep compliance records longer (7 years)
    DELETE FROM compliance_records WHERE created_at < NOW() - INTERVAL '1 day' * 2555;
    
    RAISE NOTICE 'Cleaned up audit data older than % days', retention_days;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add table comments
COMMENT ON TABLE audit_logs IS 'General system audit trail for all activities';
COMMENT ON TABLE user_activities IS 'User interaction tracking for analytics';
COMMENT ON TABLE security_events IS 'Security-related events and incidents';
COMMENT ON TABLE performance_metrics IS 'System performance monitoring data';
COMMENT ON TABLE compliance_records IS 'Regulatory compliance tracking';
COMMENT ON TABLE api_audits IS 'API usage and performance auditing';
COMMENT ON TABLE document_audits IS 'Document access and modification tracking';
