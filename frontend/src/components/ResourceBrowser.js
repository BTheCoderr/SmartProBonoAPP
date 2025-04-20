import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Container, 
  Row, 
  Col, 
  Card, 
  Button, 
  Form, 
  InputGroup, 
  Tabs, 
  Tab, 
  Badge, 
  Spinner, 
  Alert 
} from 'react-bootstrap';

// Resource type constants - must match backend
const RESOURCE_TYPE_TEMPLATE = "template";
const RESOURCE_TYPE_USER_DOCUMENT = "user_document";
const RESOURCE_TYPE_MEDIA = "media";

/**
 * ResourceBrowser component for viewing and downloading resources
 * from both GitHub Releases and Cloudinary.
 */
const ResourceBrowser = () => {
  // State management
  const [activeTab, setActiveTab] = useState(RESOURCE_TYPE_TEMPLATE);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searching, setSearching] = useState(false);
  
  // Template-specific state (GitHub)
  const [templateVersion, setTemplateVersion] = useState('latest');
  const [templateCategory, setTemplateCategory] = useState('');
  const [availableVersions, setAvailableVersions] = useState(['latest']);
  
  // User content specific state (Cloudinary)
  const [folder, setFolder] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [availableTags, setAvailableTags] = useState([]);
  
  // Load resources when tab changes or filters are updated
  useEffect(() => {
    loadResources();
  }, [activeTab, templateVersion, templateCategory, folder, selectedTags.join(',')]);
  
  // Load available versions on component mount
  useEffect(() => {
    // For a real implementation, you would fetch available releases from GitHub API
    setAvailableVersions(['latest', 'v1.0.0']);
    
    // For a real implementation, you would fetch available tags from Cloudinary
    setAvailableTags(['legal', 'contract', 'housing', 'immigration']);
  }, []);
  
  /**
   * Load resources based on current filters and active tab
   */
  const loadResources = async (overrideSearch = null) => {
    setLoading(true);
    setError(null);
    
    try {
      // Build query parameters based on resource type
      let params = { type: activeTab };
      
      if (overrideSearch !== null || searchTerm) {
        params.search = overrideSearch !== null ? overrideSearch : searchTerm;
      }
      
      // Template-specific parameters (GitHub)
      if (activeTab === RESOURCE_TYPE_TEMPLATE) {
        if (templateVersion) params.version = templateVersion;
        if (templateCategory) params.category = templateCategory;
      }
      
      // User content specific parameters (Cloudinary)
      else if (activeTab === RESOURCE_TYPE_USER_DOCUMENT || activeTab === RESOURCE_TYPE_MEDIA) {
        if (folder) params.folder = folder;
        if (selectedTags.length > 0) params.tags = selectedTags.join(',');
      }
      
      // Call the API
      const response = await axios.get('/api/resources', { params });
      setResources(response.data || []);
    } catch (err) {
      console.error('Error loading resources:', err);
      setError(`Error loading resources: ${err.response?.data?.error || err.message}`);
      setResources([]);
    } finally {
      setLoading(false);
      setSearching(false);
    }
  };
  
  /**
   * Handle search form submission
   */
  const handleSearch = (e) => {
    e.preventDefault();
    setSearching(true);
    loadResources();
  };
  
  /**
   * Download a template file from GitHub Releases
   */
  const downloadTemplate = async (templateName) => {
    try {
      const response = await axios.get(`/api/resources/${templateName}`, {
        params: { type: RESOURCE_TYPE_TEMPLATE, version: templateVersion },
        responseType: 'blob'
      });
      
      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', templateName);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error('Error downloading template:', err);
      alert('Failed to download template. Please try again.');
    }
  };
  
  /**
   * Open a Cloudinary resource
   */
  const openCloudinaryResource = async (resourceId) => {
    try {
      const response = await axios.get(`/api/resources/${resourceId}`, {
        params: { 
          type: activeTab,
          // Add any transformations if needed
        }
      });
      
      // Open the URL in a new tab
      window.open(response.data.url, '_blank');
    } catch (err) {
      console.error('Error opening resource:', err);
      alert('Failed to open resource. Please try again.');
    }
  };
  
  /**
   * Filter for only showing certain file types
   */
  const getFileTypeFilter = () => {
    if (activeTab === RESOURCE_TYPE_TEMPLATE) {
      return (
        <Form.Group className="mb-3">
          <Form.Label>Category</Form.Label>
          <Form.Control
            as="select"
            value={templateCategory}
            onChange={(e) => setTemplateCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            <option value="legal">Legal</option>
            <option value="housing">Housing</option>
            <option value="immigration">Immigration</option>
          </Form.Control>
        </Form.Group>
      );
    } else if (activeTab === RESOURCE_TYPE_USER_DOCUMENT) {
      return (
        <Form.Group className="mb-3">
          <Form.Label>Document Tags</Form.Label>
          <div>
            {availableTags.map(tag => (
              <Form.Check
                key={tag}
                inline
                type="checkbox"
                label={tag}
                checked={selectedTags.includes(tag)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedTags([...selectedTags, tag]);
                  } else {
                    setSelectedTags(selectedTags.filter(t => t !== tag));
                  }
                }}
              />
            ))}
          </div>
        </Form.Group>
      );
    } else {
      return (
        <Form.Group className="mb-3">
          <Form.Label>Media Folder</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter folder name"
            value={folder}
            onChange={(e) => setFolder(e.target.value)}
          />
        </Form.Group>
      );
    }
  };
  
  /**
   * Render resource cards based on type
   */
  const renderResourceCards = () => {
    if (resources.length === 0) {
      return (
        <Col className="text-center py-5">
          <p className="text-muted">No resources found.</p>
        </Col>
      );
    }
    
    if (activeTab === RESOURCE_TYPE_TEMPLATE) {
      return resources.map(template => (
        <Col md={4} key={template.name} className="mb-4">
          <Card>
            <Card.Body>
              <Card.Title>{template.name.split('/').pop()}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                Size: {Math.round(template.size / 1024)} KB
              </Card.Subtitle>
              <Card.Text>
                Downloads: {template.download_count || 0}
                <br />
                Updated: {new Date(template.updated_at).toLocaleDateString()}
              </Card.Text>
              <Button 
                variant="primary" 
                onClick={() => downloadTemplate(template.name)}
              >
                Download
              </Button>
            </Card.Body>
          </Card>
        </Col>
      ));
    } else {
      // Cloudinary resources (documents or media)
      return resources.map(resource => (
        <Col md={4} key={resource.public_id} className="mb-4">
          <Card>
            {activeTab === RESOURCE_TYPE_MEDIA && resource.resource_type === 'image' && (
              <Card.Img 
                variant="top" 
                src={resource.url.replace('/upload/', '/upload/w_300,h_200,c_fill/')} 
                alt={resource.public_id}
              />
            )}
            <Card.Body>
              <Card.Title>
                {resource.public_id.split('/').pop()}
              </Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                Type: {resource.resource_type}/{resource.format || 'unknown'}
              </Card.Subtitle>
              {resource.tags && resource.tags.length > 0 && (
                <div className="mb-2">
                  {resource.tags.map(tag => (
                    <Badge 
                      key={tag} 
                      bg="secondary" 
                      className="me-1"
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>
              )}
              <Card.Text>
                Created: {new Date(resource.created_at).toLocaleDateString()}
              </Card.Text>
              <Button 
                variant="primary" 
                onClick={() => openCloudinaryResource(resource.public_id)}
              >
                View
              </Button>
            </Card.Body>
          </Card>
        </Col>
      ));
    }
  };
  
  return (
    <Container className="mt-4">
      <h2>Resource Browser</h2>
      
      <Tabs
        activeKey={activeTab}
        onSelect={(key) => setActiveTab(key)}
        className="mb-4"
      >
        <Tab eventKey={RESOURCE_TYPE_TEMPLATE} title="Official Templates" />
        <Tab eventKey={RESOURCE_TYPE_USER_DOCUMENT} title="User Documents" />
        <Tab eventKey={RESOURCE_TYPE_MEDIA} title="Media" />
      </Tabs>
      
      {/* Filter and search form */}
      <Form onSubmit={handleSearch} className="mb-4">
        <Row>
          <Col md={6}>
            {getFileTypeFilter()}
          </Col>
          
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Search</Form.Label>
              <InputGroup>
                <Form.Control
                  type="text"
                  placeholder="Search resources..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button 
                  type="submit" 
                  variant="primary" 
                  disabled={searching}
                >
                  {searching ? (
                    <>
                      <Spinner
                        as="span"
                        animation="border"
                        size="sm"
                        role="status"
                        aria-hidden="true"
                      />
                      <span className="visually-hidden">Searching...</span>
                    </>
                  ) : (
                    'Search'
                  )}
                </Button>
              </InputGroup>
            </Form.Group>
            
            {activeTab === RESOURCE_TYPE_TEMPLATE && (
              <Form.Group>
                <Form.Label>Version</Form.Label>
                <Form.Control
                  as="select"
                  value={templateVersion}
                  onChange={(e) => setTemplateVersion(e.target.value)}
                >
                  {availableVersions.map(version => (
                    <option key={version} value={version}>{version}</option>
                  ))}
                </Form.Control>
              </Form.Group>
            )}
          </Col>
        </Row>
      </Form>
      
      {/* Error message */}
      {error && (
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      {/* Resources */}
      <Row>
        {loading ? (
          <Col className="text-center py-5">
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          </Col>
        ) : (
          renderResourceCards()
        )}
      </Row>
    </Container>
  );
};

export default ResourceBrowser; 