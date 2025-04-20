import React, { useState } from 'react';
import axios from 'axios';
import { 
  Container, 
  Form, 
  Button, 
  Alert, 
  ProgressBar, 
  Row, 
  Col, 
  Card 
} from 'react-bootstrap';

// Resource type constants - must match backend
const RESOURCE_TYPE_USER_DOCUMENT = "user_document";
const RESOURCE_TYPE_MEDIA = "media";

/**
 * ResourceUpload component for uploading user-generated content to Cloudinary.
 */
const ResourceUpload = () => {
  // Form state
  const [file, setFile] = useState(null);
  const [resourceType, setResourceType] = useState(RESOURCE_TYPE_USER_DOCUMENT);
  const [folder, setFolder] = useState('');
  const [tags, setTags] = useState('');
  const [metadata, setMetadata] = useState([{ key: '', value: '' }]);
  
  // UI state
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [uploadedResource, setUploadedResource] = useState(null);
  
  /**
   * Handle file selection
   */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      
      // Auto-detect resource type based on file MIME type
      if (selectedFile.type.startsWith('image/') || selectedFile.type.startsWith('video/')) {
        setResourceType(RESOURCE_TYPE_MEDIA);
      } else {
        setResourceType(RESOURCE_TYPE_USER_DOCUMENT);
      }
    }
  };
  
  /**
   * Add a new metadata field
   */
  const addMetadataField = () => {
    setMetadata([...metadata, { key: '', value: '' }]);
  };
  
  /**
   * Update a metadata field
   */
  const updateMetadataField = (index, field, value) => {
    const updatedMetadata = [...metadata];
    updatedMetadata[index][field] = value;
    setMetadata(updatedMetadata);
  };
  
  /**
   * Remove a metadata field
   */
  const removeMetadataField = (index) => {
    const updatedMetadata = metadata.filter((_, i) => i !== index);
    setMetadata(updatedMetadata);
  };
  
  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    
    // Reset state
    setError('');
    setSuccessMessage('');
    setUploadProgress(0);
    setUploading(true);
    setUploadedResource(null);
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', resourceType);
    
    if (folder) {
      formData.append('folder', folder);
    }
    
    if (tags) {
      formData.append('tags', tags);
    }
    
    // Add metadata fields
    metadata.forEach(item => {
      if (item.key && item.value) {
        formData.append(`meta_${item.key}`, item.value);
      }
    });
    
    try {
      // Upload the file
      const response = await axios.post('/api/resources', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
        }
      });
      
      // Show success message
      setSuccessMessage('File uploaded successfully!');
      setUploadedResource(response.data);
      
      // Reset form
      setFile(null);
      setTags('');
      setMetadata([{ key: '', value: '' }]);
      
      // Reset file input
      const fileInput = document.getElementById('file-upload');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      setError(err.response?.data?.error || 'Failed to upload file. Please try again.');
    } finally {
      setUploading(false);
    }
  };
  
  return (
    <Container className="mt-4">
      <h2>Upload Resource</h2>
      <p className="text-muted">
        Upload user documents and media to be stored in Cloudinary.
      </p>
      
      <Row>
        <Col md={8}>
          {/* Success message */}
          {successMessage && (
            <Alert variant="success" dismissible onClose={() => setSuccessMessage('')}>
              {successMessage}
            </Alert>
          )}
          
          {/* Error message */}
          {error && (
            <Alert variant="danger" dismissible onClose={() => setError('')}>
              {error}
            </Alert>
          )}
          
          {/* Upload form */}
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>File <span className="text-danger">*</span></Form.Label>
              <Form.Control
                id="file-upload"
                type="file"
                onChange={handleFileChange}
                required
              />
              <Form.Text className="text-muted">
                Select a file to upload. Images and videos will automatically be classified as media.
              </Form.Text>
            </Form.Group>
            
            <Form.Group className="mb-3">
              <Form.Label>Resource Type</Form.Label>
              <Form.Select
                value={resourceType}
                onChange={(e) => setResourceType(e.target.value)}
              >
                <option value={RESOURCE_TYPE_USER_DOCUMENT}>Document</option>
                <option value={RESOURCE_TYPE_MEDIA}>Media (Image/Video)</option>
              </Form.Select>
            </Form.Group>
            
            <Form.Group className="mb-3">
              <Form.Label>Folder</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g., legal/contracts"
                value={folder}
                onChange={(e) => setFolder(e.target.value)}
              />
              <Form.Text className="text-muted">
                Optional. Specify a folder path to organize your resources.
              </Form.Text>
            </Form.Group>
            
            <Form.Group className="mb-3">
              <Form.Label>Tags</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g., contract, legal, important"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
              />
              <Form.Text className="text-muted">
                Optional. Comma-separated tags to help organize and find your content.
              </Form.Text>
            </Form.Group>
            
            <Form.Group className="mb-3">
              <Form.Label>Metadata</Form.Label>
              
              {metadata.map((item, index) => (
                <Row key={index} className="mb-2">
                  <Col>
                    <Form.Control
                      placeholder="Key"
                      value={item.key}
                      onChange={(e) => updateMetadataField(index, 'key', e.target.value)}
                    />
                  </Col>
                  <Col>
                    <Form.Control
                      placeholder="Value"
                      value={item.value}
                      onChange={(e) => updateMetadataField(index, 'value', e.target.value)}
                    />
                  </Col>
                  <Col xs="auto">
                    <Button 
                      variant="outline-danger" 
                      onClick={() => removeMetadataField(index)}
                      disabled={metadata.length === 1}
                    >
                      Remove
                    </Button>
                  </Col>
                </Row>
              ))}
              
              <Button 
                variant="outline-secondary" 
                onClick={addMetadataField} 
                size="sm" 
                className="mt-2"
              >
                Add Metadata Field
              </Button>
            </Form.Group>
            
            {uploading && (
              <ProgressBar 
                now={uploadProgress} 
                label={`${uploadProgress}%`} 
                className="mb-3" 
              />
            )}
            
            <Button 
              variant="primary" 
              type="submit" 
              disabled={uploading || !file}
            >
              {uploading ? 'Uploading...' : 'Upload Resource'}
            </Button>
          </Form>
        </Col>
        
        <Col md={4}>
          {/* Preview of uploaded resource */}
          {uploadedResource && (
            <Card className="mt-3">
              <Card.Header>Uploaded Resource</Card.Header>
              <Card.Body>
                {uploadedResource.resource_type === 'image' && (
                  <img 
                    src={uploadedResource.url} 
                    alt="Uploaded content" 
                    className="img-fluid mb-3" 
                  />
                )}
                
                <dl>
                  <dt>Resource ID:</dt>
                  <dd>{uploadedResource.id}</dd>
                  
                  <dt>Type:</dt>
                  <dd>{uploadedResource.resource_type}/{uploadedResource.format || 'unknown'}</dd>
                  
                  <dt>URL:</dt>
                  <dd>
                    <a href={uploadedResource.url} target="_blank" rel="noopener noreferrer">
                      View Resource
                    </a>
                  </dd>
                </dl>
              </Card.Body>
            </Card>
          )}
          
          {/* Information card */}
          <Card className="mt-3">
            <Card.Header>About Resource Management</Card.Header>
            <Card.Body>
              <h5>Two-System Approach</h5>
              <p>
                SmartProBono uses a hybrid approach to resource management:
              </p>
              
              <h6>1. Official Templates</h6>
              <p>
                Stored in GitHub Releases, managed by project maintainers.
              </p>
              
              <h6>2. User Content</h6>
              <p>
                Uploaded here and stored in Cloudinary for fast, secure access.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ResourceUpload; 