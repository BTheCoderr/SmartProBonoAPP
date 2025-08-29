-- Audit System Database Schema for SmartProBono
-- This schema extends the existing Supabase database with comprehensive auditing capabilities

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
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
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
    metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- User interaction tracking
CREATE TABLE user_activities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    session_id varchar(255),
    activity_type varchar(100) NOT NULL, -- login, logout, page_view, etc.
    page_url varchar(500),
    page_title varchar(255),
    action varchar(100), -- click, submit, download, etc.
    element_id varchar(255), -- ID of clicked element
    element_class varchar(255), -- Class of clicked element
    duration_seconds integer, -- Time spent on page
    referrer varchar(500),
    ip_address varchar(45),
    user_agent text,
    device_type varchar(50), -- desktop, mobile, tablet
    browser varchar(100),
    os varchar(100),
    metadata text, -- Additional JSON data
    created_at timestamp DEFAULT now() NOT NULL
);

-- Security-related events
CREATE TABLE security_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type varchar(100) NOT NULL, -- failed_login, suspicious_activity, etc.
    severity audit_severity NOT NULL,
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    ip_address varchar(45),
    user_agent text,
    endpoint varchar(255),
    attack_type varchar(100), -- brute_force, sql_injection, etc.
    blocked boolean DEFAULT false,
    reason text,
    response_action varchar(100), -- block_ip, lock_account, etc.
    metadata text,
    created_at timestamp DEFAULT now() NOT NULL
);

-- System performance data
CREATE TABLE performance_metrics (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_type varchar(100) NOT NULL, -- response_time, memory_usage, etc.
    endpoint varchar(255),
    value decimal NOT NULL,
    unit varchar(20), -- ms, MB, %, etc.
    threshold decimal, -- Alert threshold
    exceeded_threshold boolean DEFAULT false,
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    session_id varchar(255),
    metadata text,
    created_at timestamp DEFAULT now() NOT NULL
);

-- Regulatory compliance tracking
CREATE TABLE compliance_records (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    record_type varchar(100) NOT NULL, -- gdpr_request, data_retention, etc.
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    request_id varchar(255), -- External request ID
    status varchar(50) NOT NULL, -- pending, completed, failed
    description text,
    data_subject varchar(255), -- Person whose data is involved
    data_types text, -- JSON array of data types
    legal_basis varchar(100), -- consent, legitimate_interest, etc.
    retention_period integer, -- Days
    processed_by uuid REFERENCES users(id) ON DELETE SET NULL,
    processed_at timestamp,
    metadata text,
    created_at timestamp DEFAULT now() NOT NULL,
    updated_at timestamp DEFAULT now()
);

-- API usage auditing
CREATE TABLE api_audits (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint varchar(255) NOT NULL,
    method varchar(10) NOT NULL,
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    api_key_id varchar(255),
    ip_address varchar(45),
    user_agent text,
    request_size integer, -- Bytes
    response_size integer, -- Bytes
    response_time_ms integer NOT NULL,
    status_code integer NOT NULL,
    rate_limit_hit boolean DEFAULT false,
    rate_limit_remaining integer,
    error_message text,
    metadata text,
    created_at timestamp DEFAULT now() NOT NULL
);

-- Document access and modification tracking
CREATE TABLE document_audits (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid REFERENCES documents(id) ON DELETE CASCADE NOT NULL,
    user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    action varchar(50) NOT NULL, -- view, download, edit, delete, share
    ip_address varchar(45),
    user_agent text,
    file_size integer,
    processing_time_ms integer,
    version varchar(50),
    changes_made text, -- JSON of changes
    shared_with text, -- JSON of shared users
    metadata text,
    created_at timestamp DEFAULT now() NOT NULL
);

-- Create indexes for better performance
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_severity ON audit_logs(severity);
CREATE INDEX idx_audit_logs_endpoint ON audit_logs(endpoint);

CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX idx_user_activities_activity_type ON user_activities(activity_type);
CREATE INDEX idx_user_activities_created_at ON user_activities(created_at);
CREATE INDEX idx_user_activities_session_id ON user_activities(session_id);

CREATE INDEX idx_security_events_severity ON security_events(severity);
CREATE INDEX idx_security_events_created_at ON security_events(created_at);
CREATE INDEX idx_security_events_event_type ON security_events(event_type);
CREATE INDEX idx_security_events_ip_address ON security_events(ip_address);

CREATE INDEX idx_performance_metrics_metric_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_created_at ON performance_metrics(created_at);
CREATE INDEX idx_performance_metrics_endpoint ON performance_metrics(endpoint);

CREATE INDEX idx_compliance_records_record_type ON compliance_records(record_type);
CREATE INDEX idx_compliance_records_status ON compliance_records(status);
CREATE INDEX idx_compliance_records_created_at ON compliance_records(created_at);

CREATE INDEX idx_api_audits_endpoint ON api_audits(endpoint);
CREATE INDEX idx_api_audits_created_at ON api_audits(created_at);
CREATE INDEX idx_api_audits_user_id ON api_audits(user_id);

CREATE INDEX idx_document_audits_document_id ON document_audits(document_id);
CREATE INDEX idx_document_audits_user_id ON document_audits(user_id);
CREATE INDEX idx_document_audits_action ON document_audits(action);
CREATE INDEX idx_document_audits_created_at ON document_audits(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_audits ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for audit_logs
CREATE POLICY "Admins can view all audit logs" ON audit_logs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

CREATE POLICY "Users can view their own audit logs" ON audit_logs
    FOR SELECT USING (auth.uid() = user_id);

-- Create RLS policies for user_activities
CREATE POLICY "Users can view their own activities" ON user_activities
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all user activities" ON user_activities
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

-- Create RLS policies for security_events
CREATE POLICY "Admins can view all security events" ON security_events
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

CREATE POLICY "Users can view their own security events" ON security_events
    FOR SELECT USING (auth.uid() = user_id);

-- Create RLS policies for performance_metrics
CREATE POLICY "Admins can view all performance metrics" ON performance_metrics
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

CREATE POLICY "Users can view their own performance metrics" ON performance_metrics
    FOR SELECT USING (auth.uid() = user_id);

-- Create RLS policies for compliance_records
CREATE POLICY "Admins can view all compliance records" ON compliance_records
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

CREATE POLICY "Users can view their own compliance records" ON compliance_records
    FOR SELECT USING (auth.uid() = user_id);

-- Create RLS policies for api_audits
CREATE POLICY "Admins can view all API audits" ON api_audits
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

CREATE POLICY "Users can view their own API audits" ON api_audits
    FOR SELECT USING (auth.uid() = user_id);

-- Create RLS policies for document_audits
CREATE POLICY "Users can view their own document audits" ON document_audits
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all document audits" ON document_audits
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE users.id = auth.uid() 
            AND users.role = 'admin'
        )
    );

-- Create functions for automatic audit logging
CREATE OR REPLACE FUNCTION log_audit_event(
    p_event_type audit_event_type,
    p_action varchar(100),
    p_user_id uuid DEFAULT NULL,
    p_resource_id varchar(255) DEFAULT NULL,
    p_resource_type varchar(100) DEFAULT NULL,
    p_description text DEFAULT NULL,
    p_severity audit_severity DEFAULT 'low',
    p_metadata jsonb DEFAULT NULL
) RETURNS uuid AS $$
DECLARE
    audit_id uuid;
BEGIN
    INSERT INTO audit_logs (
        event_type, action, user_id, resource_id, resource_type,
        description, severity, metadata, created_at
    ) VALUES (
        p_event_type, p_action, p_user_id, p_resource_id, p_resource_type,
        p_description, p_severity, p_metadata::text, now()
    ) RETURNING id INTO audit_id;
    
    RETURN audit_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function for logging security events
CREATE OR REPLACE FUNCTION log_security_event(
    p_event_type varchar(100),
    p_severity audit_severity,
    p_user_id uuid DEFAULT NULL,
    p_ip_address varchar(45) DEFAULT NULL,
    p_reason text DEFAULT NULL,
    p_blocked boolean DEFAULT false,
    p_metadata jsonb DEFAULT NULL
) RETURNS uuid AS $$
DECLARE
    security_id uuid;
BEGIN
    INSERT INTO security_events (
        event_type, severity, user_id, ip_address, reason, blocked, metadata, created_at
    ) VALUES (
        p_event_type, p_severity, p_user_id, p_ip_address, p_reason, p_blocked, p_metadata::text, now()
    ) RETURNING id INTO security_id;
    
    RETURN security_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function for logging performance metrics
CREATE OR REPLACE FUNCTION log_performance_metric(
    p_metric_type varchar(100),
    p_value decimal,
    p_unit varchar(20) DEFAULT NULL,
    p_threshold decimal DEFAULT NULL,
    p_endpoint varchar(255) DEFAULT NULL,
    p_user_id uuid DEFAULT NULL,
    p_metadata jsonb DEFAULT NULL
) RETURNS uuid AS $$
DECLARE
    metric_id uuid;
    exceeded boolean := false;
BEGIN
    IF p_threshold IS NOT NULL AND p_value > p_threshold THEN
        exceeded := true;
    END IF;
    
    INSERT INTO performance_metrics (
        metric_type, value, unit, threshold, exceeded_threshold,
        endpoint, user_id, metadata, created_at
    ) VALUES (
        p_metric_type, p_value, p_unit, p_threshold, exceeded,
        p_endpoint, p_user_id, p_metadata::text, now()
    ) RETURNING id INTO metric_id;
    
    RETURN metric_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create triggers for automatic audit logging on data changes
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        PERFORM log_audit_event(
            'data_modification',
            'CREATE',
            NEW.user_id,
            NEW.id::varchar,
            TG_TABLE_NAME,
            'Record created in ' || TG_TABLE_NAME,
            'low',
            row_to_json(NEW)
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        PERFORM log_audit_event(
            'data_modification',
            'UPDATE',
            NEW.user_id,
            NEW.id::varchar,
            TG_TABLE_NAME,
            'Record updated in ' || TG_TABLE_NAME,
            'low',
            json_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW))
        );
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        PERFORM log_audit_event(
            'data_modification',
            'DELETE',
            OLD.user_id,
            OLD.id::varchar,
            TG_TABLE_NAME,
            'Record deleted from ' || TG_TABLE_NAME,
            'medium',
            row_to_json(OLD)
        );
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers for key tables
CREATE TRIGGER audit_users_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_documents_trigger
    AFTER INSERT OR UPDATE OR DELETE ON documents
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_cases_trigger
    AFTER INSERT OR UPDATE OR DELETE ON cases
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_conversations_trigger
    AFTER INSERT OR UPDATE OR DELETE ON conversations
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Create view for audit dashboard
CREATE VIEW audit_dashboard_view AS
SELECT 
    'audit_logs' as table_name,
    event_type,
    severity,
    COUNT(*) as count,
    DATE_TRUNC('hour', created_at) as hour
FROM audit_logs
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY event_type, severity, hour

UNION ALL

SELECT 
    'security_events' as table_name,
    event_type::audit_event_type,
    severity,
    COUNT(*) as count,
    DATE_TRUNC('hour', created_at) as hour
FROM security_events
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY event_type::audit_event_type, severity, hour

UNION ALL

SELECT 
    'user_activities' as table_name,
    'user_activity'::audit_event_type,
    'low'::audit_severity,
    COUNT(*) as count,
    DATE_TRUNC('hour', created_at) as hour
FROM user_activities
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY hour;

-- Grant permissions
GRANT SELECT ON audit_dashboard_view TO authenticated;
GRANT EXECUTE ON FUNCTION log_audit_event TO authenticated;
GRANT EXECUTE ON FUNCTION log_security_event TO authenticated;
GRANT EXECUTE ON FUNCTION log_performance_metric TO authenticated;

-- Create cleanup function for old audit data
CREATE OR REPLACE FUNCTION cleanup_old_audit_data(retention_days integer DEFAULT 90)
RETURNS void AS $$
BEGIN
    -- Delete old audit logs (keep only specified days)
    DELETE FROM audit_logs WHERE created_at < NOW() - (retention_days || ' days')::interval;
    
    -- Delete old user activities
    DELETE FROM user_activities WHERE created_at < NOW() - (retention_days || ' days')::interval;
    
    -- Delete old performance metrics (keep only 30 days by default)
    DELETE FROM performance_metrics WHERE created_at < NOW() - (30 || ' days')::interval;
    
    -- Delete old API audits
    DELETE FROM api_audits WHERE created_at < NOW() - (retention_days || ' days')::interval;
    
    -- Keep security events longer (1 year)
    DELETE FROM security_events WHERE created_at < NOW() - (365 || ' days')::interval;
    
    -- Keep compliance records longer (7 years)
    DELETE FROM compliance_records WHERE created_at < NOW() - (2555 || ' days')::interval;
    
    RAISE NOTICE 'Cleaned up audit data older than % days', retention_days;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create scheduled cleanup (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-audit-data', '0 2 * * *', 'SELECT cleanup_old_audit_data(90);');

COMMENT ON TABLE audit_logs IS 'General system audit trail for all activities';
COMMENT ON TABLE user_activities IS 'User interaction tracking for analytics';
COMMENT ON TABLE security_events IS 'Security-related events and incidents';
COMMENT ON TABLE performance_metrics IS 'System performance monitoring data';
COMMENT ON TABLE compliance_records IS 'Regulatory compliance tracking';
COMMENT ON TABLE api_audits IS 'API usage and performance auditing';
COMMENT ON TABLE document_audits IS 'Document access and modification tracking';
