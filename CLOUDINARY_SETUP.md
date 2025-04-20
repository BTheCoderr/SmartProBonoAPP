# Cloudinary Setup for SmartProBono

This guide explains how to set up and use Cloudinary for media storage in the SmartProBono project.

## What is Cloudinary?

[Cloudinary](https://cloudinary.com/) is a cloud-based service that provides an end-to-end image and video management solution including uploads, storage, manipulations, optimizations and delivery.

In SmartProBono, we use Cloudinary for:
- Storing legal documents
- Managing case evidence files
- Storing user profile images
- Hosting shared legal resources
- Managing document templates

## Setup Instructions

### 1. Create a Cloudinary Account

1. Sign up for a free Cloudinary account at [https://cloudinary.com/users/register/free](https://cloudinary.com/users/register/free)
2. After registration, you'll be taken to your dashboard where you can find your account details

### 2. Get Your API Credentials

From your Cloudinary dashboard:
1. Note your **Cloud name**
2. Find your **API Key** and **API Secret** under the "Security" section

### 3. Configure Environment Variables

Add your Cloudinary credentials to your environment:

#### For Local Development

Create a `.env` file in the `backend` directory with the following contents:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

#### For GitHub Actions

Add the following secrets to your GitHub repository:
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

### 4. Run the Cloudinary Setup

The initial setup of folders and upload presets can be done automatically:

```bash
python -m backend.scripts.setup_cloudinary
```

Or trigger the GitHub Actions workflow:

```bash
git push origin main
```

## Folder Structure

The following folder structure is created in your Cloudinary account:

- `legal_documents`: Legal documents and forms
- `case_evidence`: Evidence files for cases
- `profile_images`: User profile images
- `shared_resources`: Shared legal resource files
- `templates`: Document templates

## Upload Presets

We've configured several upload presets with specific settings:

1. **legal_documents_preset**:
   - For PDF, DOCX, DOC, RTF, and TXT files
   - Uses secure access mode

2. **case_evidence_preset**:
   - For images, PDFs, audio, and video files
   - Uses secure access mode

3. **profile_images_preset**:
   - For JPG and PNG images
   - Automatically resizes to max 500x500
   - Uses public access mode

## Using Cloudinary in the Application

### Backend

The CloudinaryService class in `backend/services/cloudinary_service.py` provides methods for:

- Uploading files: `upload_file()`
- Retrieving file URLs: `get_file_url()`
- Deleting files: `delete_file()`
- Listing files: `list_files()`
- Getting file details: `get_file_details()`

Example usage:

```python
from backend.services.cloudinary_service import CloudinaryService

# Initialize the service
cloudinary_service = CloudinaryService()

# Upload a file
result = cloudinary_service.upload_file(
    file="path/to/document.pdf",
    resource_type="raw",
    folder="legal_documents",
    tags=["contract", "client123"]
)

# Get the URL
file_url = result["secure_url"]
```

### Frontend

To display Cloudinary images or files in the frontend:

```jsx
import React from 'react';

const CloudinaryImage = ({ publicId, alt }) => {
  const url = `https://res.cloudinary.com/${process.env.REACT_APP_CLOUDINARY_CLOUD_NAME}/image/upload/${publicId}`;
  
  return <img src={url} alt={alt} />;
};

export default CloudinaryImage;
```

## Security Considerations

- Cloudinary resources are accessed via HTTPS
- Legal documents and case evidence use authenticated access mode
- Public IDs are unique and randomized
- Upload presets control what types of files can be uploaded
- The Cloudinary API Secret should never be exposed in frontend code

## Monitoring and Management

You can monitor your Cloudinary usage and manage files through:

1. The Cloudinary Dashboard at [https://cloudinary.com/console](https://cloudinary.com/console)
2. The Media Library at [https://cloudinary.com/console/media_library](https://cloudinary.com/console/media_library)

## Additional Resources

- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Cloudinary Python SDK](https://cloudinary.com/documentation/django_integration)
- [Cloudinary JavaScript SDK](https://cloudinary.com/documentation/javascript_integration) 