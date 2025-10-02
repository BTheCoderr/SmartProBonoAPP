import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Alert, Tabs, Tab } from 'react-bootstrap';
import { 
  Bot, 
  Case, 
  Users, 
  FileText, 
  Search, 
  Bell, 
  Calendar,
  TrendingUp,
  Activity,
  Shield,
  Settings,
  Plus,
  BarChart3,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';
import SmartProBonoAgent from './SmartProBonoAgent';
import './SmartProBonoDashboard.css';

const SmartProBonoDashboard = ({ user, onAgentToggle }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [showAgent, setShowAgent] = useState(false);
  const [dashboardStats, setDashboardStats] = useState({
    totalCases: 0,
    activeCases: 0,
    clients: 0,
    documents: 0,
    notifications: 0,
    recentActivity: []
  });

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      // This would integrate with your existing analytics/statistics APIs
      // For now, we'll use mock data
      setDashboardStats({
        totalCases: 24,
        activeCases: 8,
        clients: 156,
        documents: 89,
        notifications: 3,
        recentActivity: [
          { id: 1, type: 'case_created', message: 'New immigration case created for John Smith', time: '2 hours ago' },
          { id: 2, type: 'document_analyzed', message: 'Contract analysis completed for Case #1234', time: '4 hours ago' },
          { id: 3, type: 'notification_sent', message: 'Status update sent to client Sarah Johnson', time: '6 hours ago' }
        ]
      });
    } catch (error) {
      console.error('Error loading dashboard stats:', error);
    }
  };

  const handleAgentToggle = () => {
    const newShowAgent = !showAgent;
    setShowAgent(newShowAgent);
    if (onAgentToggle) {
      onAgentToggle(newShowAgent);
    }
  };

  const getRoleBasedFeatures = () => {
    switch (user?.role) {
      case 'lawyer':
        return [
          { title: 'Case Management', icon: <Case size={20} />, description: 'Manage your cases and clients' },
          { title: 'Document Analysis', icon: <FileText size={20} />, description: 'AI-powered document review' },
          { title: 'Legal Research', icon: <Search size={20} />, description: 'Search case law and precedents' },
          { title: 'Client Communication', icon: <Users size={20} />, description: 'Manage client relationships' }
        ];
      case 'client':
        return [
          { title: 'My Cases', icon: <Case size={20} />, description: 'Track your legal cases' },
          { title: 'Documents', icon: <FileText size={20} />, description: 'Access your legal documents' },
          { title: 'Communications', icon: <Bell size={20} />, description: 'Messages from your lawyer' },
          { title: 'Legal Help', icon: <Shield size={20} />, description: 'Get legal guidance and support' }
        ];
      case 'admin':
        return [
          { title: 'System Overview', icon: <BarChart3 size={20} />, description: 'Platform analytics and metrics' },
          { title: 'User Management', icon: <Users size={20} />, description: 'Manage users and permissions' },
          { title: 'System Health', icon: <Activity size={20} />, description: 'Monitor system performance' },
          { title: 'Settings', icon: <Settings size={20} />, description: 'Configure platform settings' }
        ];
      default:
        return [
          { title: 'Legal Assistance', icon: <Shield size={20} />, description: 'Get help with legal matters' },
          { title: 'Document Review', icon: <FileText size={20} />, description: 'Analyze your documents' },
          { title: 'Case Information', icon: <Case size={20} />, description: 'Learn about your case' },
          { title: 'Support', icon: <Bell size={20} />, description: 'Contact support team' }
        ];
    }
  };

  const getActivityIcon = (type) => {
    switch (type) {
      case 'case_created': return <Case size={16} />;
      case 'document_analyzed': return <FileText size={16} />;
      case 'notification_sent': return <Bell size={16} />;
      default: return <Activity size={16} />;
    }
  };

  const getActivityColor = (type) => {
    switch (type) {
      case 'case_created': return 'success';
      case 'document_analyzed': return 'info';
      case 'notification_sent': return 'warning';
      default: return 'secondary';
    }
  };

  if (showAgent) {
    return (
      <div className="smartprobono-dashboard agent-mode">
        <SmartProBonoAgent 
          user={user} 
          onClose={() => setShowAgent(false)} 
        />
      </div>
    );
  }

  return (
    <div className="smartprobono-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="welcome-section">
            <h2>Welcome back, {user?.username || 'User'}!</h2>
            <p className="text-muted">
              {user?.role === 'lawyer' ? 'Manage your legal practice with AI assistance' :
               user?.role === 'client' ? 'Track your legal cases and get support' :
               user?.role === 'admin' ? 'Monitor and manage the SmartProBono platform' :
               'Get legal assistance and support'}
            </p>
          </div>
          <div className="header-actions">
            <Button 
              variant="primary" 
              onClick={handleAgentToggle}
              className="agent-toggle-btn"
            >
              <Bot size={20} className="me-2" />
              Open AI Agent
            </Button>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <Row className="stats-row">
        <Col md={3}>
          <Card className="stat-card">
            <Card.Body>
              <div className="stat-content">
                <div className="stat-icon cases">
                  <Case size={24} />
                </div>
                <div className="stat-info">
                  <h3>{dashboardStats.totalCases}</h3>
                  <p>Total Cases</p>
                  <Badge variant="success">{dashboardStats.activeCases} Active</Badge>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="stat-card">
            <Card.Body>
              <div className="stat-content">
                <div className="stat-icon clients">
                  <Users size={24} />
                </div>
                <div className="stat-info">
                  <h3>{dashboardStats.clients}</h3>
                  <p>Clients</p>
                  <Badge variant="info">All Users</Badge>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="stat-card">
            <Card.Body>
              <div className="stat-content">
                <div className="stat-icon documents">
                  <FileText size={24} />
                </div>
                <div className="stat-info">
                  <h3>{dashboardStats.documents}</h3>
                  <p>Documents</p>
                  <Badge variant="warning">Processed</Badge>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="stat-card">
            <Card.Body>
              <div className="stat-content">
                <div className="stat-icon notifications">
                  <Bell size={24} />
                </div>
                <div className="stat-info">
                  <h3>{dashboardStats.notifications}</h3>
                  <p>Notifications</p>
                  <Badge variant="danger">New</Badge>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Main Content */}
      <Row className="main-content">
        <Col lg={8}>
          <Tabs activeKey={activeTab} onSelect={setActiveTab} className="dashboard-tabs">
            <Tab eventKey="overview" title="Overview">
              <div className="overview-content">
                <Row>
                  <Col md={6}>
                    <Card className="feature-grid-card">
                      <Card.Header>
                        <h5>Quick Actions</h5>
                      </Card.Header>
                      <Card.Body>
                        <div className="feature-grid">
                          {getRoleBasedFeatures().slice(0, 4).map((feature, index) => (
                            <div key={index} className="feature-item">
                              <div className="feature-icon">
                                {feature.icon}
                              </div>
                              <div className="feature-content">
                                <h6>{feature.title}</h6>
                                <p>{feature.description}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </Card.Body>
                    </Card>
                  </Col>
                  <Col md={6}>
                    <Card className="activity-card">
                      <Card.Header>
                        <h5>Recent Activity</h5>
                      </Card.Header>
                      <Card.Body>
                        <div className="activity-list">
                          {dashboardStats.recentActivity.map((activity) => (
                            <div key={activity.id} className="activity-item">
                              <div className={`activity-icon ${getActivityColor(activity.type)}`}>
                                {getActivityIcon(activity.type)}
                              </div>
                              <div className="activity-content">
                                <p className="activity-message">{activity.message}</p>
                                <small className="activity-time">{activity.time}</small>
                              </div>
                            </div>
                          ))}
                        </div>
                      </Card.Body>
                    </Card>
                  </Col>
                </Row>
              </div>
            </Tab>

            <Tab eventKey="cases" title="Cases">
              <div className="cases-content">
                <div className="content-header">
                  <h4>Case Management</h4>
                  <Button variant="primary" size="sm">
                    <Plus size={16} className="me-2" />
                    New Case
                  </Button>
                </div>
                <Alert variant="info">
                  <Bot size={16} className="me-2" />
                  Use the AI Agent to create cases, update status, and manage your legal cases efficiently.
                </Alert>
                <p>Case management content would go here...</p>
              </div>
            </Tab>

            <Tab eventKey="documents" title="Documents">
              <div className="documents-content">
                <div className="content-header">
                  <h4>Document Management</h4>
                  <Button variant="primary" size="sm">
                    <Plus size={16} className="me-2" />
                    Upload Document
                  </Button>
                </div>
                <Alert variant="info">
                  <FileText size={16} className="me-2" />
                  Upload documents and use the AI Agent to analyze them for compliance, insights, and legal review.
                </Alert>
                <p>Document management content would go here...</p>
              </div>
            </Tab>

            <Tab eventKey="research" title="Research">
              <div className="research-content">
                <div className="content-header">
                  <h4>Legal Research</h4>
                  <Button variant="primary" size="sm">
                    <Search size={16} className="me-2" />
                    Search Case Law
                  </Button>
                </div>
                <Alert variant="info">
                  <Search size={16} className="me-2" />
                  Use the AI Agent to search case law, analyze legal precedents, and research relevant legal information.
                </Alert>
                <p>Legal research content would go here...</p>
              </div>
            </Tab>
          </Tabs>
        </Col>

        <Col lg={4}>
          <div className="sidebar">
            <Card className="agent-promo-card">
              <Card.Body>
                <div className="agent-promo-content">
                  <div className="agent-icon-large">
                    <Bot size={32} />
                  </div>
                  <h5>AI Agent Available</h5>
                  <p>Get instant help with legal tasks using our SmartProBono AI Agent.</p>
                  <Button 
                    variant="primary" 
                    size="sm" 
                    onClick={handleAgentToggle}
                    className="w-100"
                  >
                    <Bot size={16} className="me-2" />
                    Open AI Agent
                  </Button>
                </div>
              </Card.Body>
            </Card>

            <Card className="help-card">
              <Card.Header>
                <h6>Need Help?</h6>
              </Card.Header>
              <Card.Body>
                <div className="help-items">
                  <div className="help-item">
                    <CheckCircle size={16} className="text-success me-2" />
                    <span>Create and manage cases</span>
                  </div>
                  <div className="help-item">
                    <CheckCircle size={16} className="text-success me-2" />
                    <span>Analyze legal documents</span>
                  </div>
                  <div className="help-item">
                    <CheckCircle size={16} className="text-success me-2" />
                    <span>Search case law</span>
                  </div>
                  <div className="help-item">
                    <CheckCircle size={16} className="text-success me-2" />
                    <span>Send notifications</span>
                  </div>
                </div>
              </Card.Body>
            </Card>

            <Card className="status-card">
              <Card.Header>
                <h6>System Status</h6>
              </Card.Header>
              <Card.Body>
                <div className="status-items">
                  <div className="status-item">
                    <div className="status-indicator online"></div>
                    <span>AI Agent</span>
                    <Badge variant="success" size="sm">Online</Badge>
                  </div>
                  <div className="status-item">
                    <div className="status-indicator online"></div>
                    <span>Database</span>
                    <Badge variant="success" size="sm">Connected</Badge>
                  </div>
                  <div className="status-item">
                    <div className="status-indicator online"></div>
                    <span>API Services</span>
                    <Badge variant="success" size="sm">Active</Badge>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default SmartProBonoDashboard;
