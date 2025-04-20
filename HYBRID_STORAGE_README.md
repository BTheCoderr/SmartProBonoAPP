# SmartProBono Hybrid Storage System

SmartProBono uses a hybrid approach to resource management, leveraging both GitHub Releases and Cloudinary.

## System Overview

### 1. GitHub Releases for Official Templates
* Legal document templates
* Form templates
* Official process documents
* Version controlled with the codebase

### 2. Cloudinary for User-Generated Content
* User-uploaded documents
* Images and media content
* Generated PDFs and reports
* Delivered through Cloudinary's global CDN

## Setting Up

1. Configure GitHub Releases in `.env`:
   ```
   GITHUB_REPO=SmartProBonoProject/SmartProBono
   GITHUB_TOKEN=your_github_token_here  # Only needed for private repositories
   ```

2. Configure Cloudinary in `.env`:
   ```
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

3. Access resources through the unified API:
   * GET `/api/resources` - List resources with filtering
   * GET `/api/resources/:id` - Get a specific resource
   * POST `/api/resources` - Upload user content to Cloudinary
   * DELETE `/api/resources/:id` - Delete user content

## Usage Examples

### Browse Templates
```javascript
// Frontend example
fetch('/api/resources?type=template&category=legal')
  .then(response => response.json())
  .then(templates => {
    // Display templates
  });
```

### Upload User Document
```javascript
// Frontend example
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('type', 'user_document');
formData.append('tags', 'contract,important');
formData.append('meta_client', 'John Doe');

fetch('/api/resources', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(result => {
  // Handle successful upload
});
```

### Get Template
```javascript
// Download a template
window.location.href = `/api/resources/legal/contract.docx?type=template`;
```

### Display Media with Transformations
```javascript
// Get an image with transformations
fetch(`/api/resources/image123?type=media&t_width=300&t_height=200&t_crop=fill`)
  .then(response => response.json())
  .then(data => {
    imageElement.src = data.url;
  });
```

## Best Practices

### For Templates
* Organize templates in subdirectories by category
* Version templates semantically with code releases
* Use consistent variable placeholders

### For User Content
* Apply appropriate tags for easy filtering
* Use logical folder hierarchies
* Add metadata for searchability

## Security Considerations

* GitHub token should have minimal permissions
* Use signed URLs for secure access to Cloudinary resources
* Implement authentication for uploads and sensitive content 