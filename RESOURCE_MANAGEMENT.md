# SmartProBono Resource Management

SmartProBono uses a hybrid approach to resource management, leveraging the strengths of both GitHub Releases and Cloudinary to handle different types of resources.

## Overview

Our resource management system is designed to handle two main types of content:

1. **Official Templates** - Stored in GitHub Releases, versioned alongside code releases
2. **User-Generated Content** - Stored in Cloudinary with CDN delivery and transformation capabilities

This approach gives us the best of both worlds: tight integration with our code versioning for official templates, and optimized media handling for user-uploaded content.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  SmartPro   │     │  Resource   │     │   GitHub    │
│  Bono App   ├────►│   Manager   ├────►│  Releases   │
│             │     │             │     │             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │                  ▲
                           │                  │
                           │                  │
                           │                  │
                           ▼                  │
                    ┌─────────────┐     ┌─────┴───────┐
                    │             │     │             │
                    │  Cloudinary │     │  Templates  │
                    │  Storage    │     │  Directory  │
                    │             │     │             │
                    └─────────────┘     └─────────────┘
```

## 1. GitHub Releases for Official Templates

### What's Stored Here
- Legal document templates
- Form templates
- Official process documents
- Any content that should be version-controlled with the code

### How It Works
1. Templates are stored in the `templates/` directory in the repository
2. When we create a release (e.g., `v1.0.0`), these templates become part of that release
3. The backend API serves these templates on demand, caching them locally
4. Templates are versioned, allowing users to access both the latest and specific historical versions

### Benefits
- Version control aligned with code
- History tracking and changelogs
- Free storage as part of GitHub
- Community contributors can submit templates via pull requests

## 2. Cloudinary for User-Generated Content

### What's Stored Here
- User-uploaded documents
- Images and media content
- Generated PDFs and reports
- Any content created or uploaded by users

### How It Works
1. Files are uploaded through our API to Cloudinary
2. Cloudinary stores them with metadata, tags, and in organized folders
3. Content is delivered via Cloudinary's global CDN
4. For images and PDFs, on-the-fly transformations are available

### Benefits
- CDN for fast global access
- Image and document transformations (resize, crop, format conversion)
- Generous free tier (25GB storage, 25GB monthly bandwidth)
- Designed specifically for media assets

## Implementation Details

### Environment Configuration

Both systems require configuration in your environment:

```
# GitHub Release Configuration
GITHUB_REPO=SmartProBonoProject/SmartProBono
GITHUB_TOKEN=your_github_token_here  # Only needed for private repositories

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### API Endpoints

The following endpoints are available for resource management:

- `GET /api/resources` - List resources with filtering
- `GET /api/resources/:id` - Get a specific resource
- `POST /api/resources` - Upload a new user resource
- `DELETE /api/resources/:id` - Delete a user resource

All endpoints accept a `type` parameter to specify which backend to use:
- `template` - Official templates from GitHub Releases
- `user_document` - User documents from Cloudinary
- `media` - Media files from Cloudinary

### Frontend Components

Two main React components are provided:
1. `ResourceBrowser.js` - For browsing resources from both backends
2. `ResourceUpload.js` - For uploading user-generated content

## Getting Started

### Setting Up GitHub Releases

1. Add your templates to the `templates/` directory
2. Create a GitHub release with a semantic version (e.g., `v1.0.0`)
3. The templates will automatically be available through the API

### Setting Up Cloudinary

1. Create a free Cloudinary account at https://cloudinary.com/
2. Get your Cloud Name, API Key, and API Secret from the dashboard
3. Add these credentials to your `.env` file
4. Use the `ResourceUpload` component to start uploading content

## Best Practices

### For Templates

- Keep templates in appropriate category subdirectories: `templates/legal/`, `templates/housing/`, etc.
- Use variables in double curly braces: `{{variable_name}}`
- Include a README.md with each template explaining its purpose and variables
- Version templates semantically with the code

### For User Content

- Use logical folder hierarchies in Cloudinary (e.g., `users/user_id/documents/`)
- Apply consistent tags for easier filtering
- Add metadata for searchability
- Leverage Cloudinary's image transformations for thumbnails and previews

## Security Considerations

- GitHub token should have minimal permissions (read-only if possible)
- Cloudinary resources should use signed URLs for secure access
- Set up proper upload restrictions in Cloudinary to prevent abuse
- Implement authentication for user content uploads and access

## Monitoring and Maintenance

### GitHub Releases
- Monitor space usage in releases
- Periodically clean up old releases if necessary
- Track release download counts for analytics

### Cloudinary
- Watch bandwidth and storage usage
- Set up usage alerts to avoid unexpected charges
- Periodically clean up unused resources

## Troubleshooting

### Common GitHub Issues
- Missing templates: Check that they were included in the release
- Access issues: Verify GitHub token permissions
- Version conflicts: Ensure you're requesting the correct version

### Common Cloudinary Issues
- Upload failures: Check credentials and permissions
- Missing resources: Verify folder paths and tags
- Transformation errors: Check parameters and supported formats 