# SmartProBono GitHub Actions

This directory contains GitHub Actions workflows for automating the testing, building, and deployment of the SmartProBono application.

## Workflows

### 1. CI/CD Pipeline (`ci.yml`)

The main continuous integration and continuous deployment pipeline that runs on every push to the main and develop branches, as well as on pull requests.

This workflow:
- Runs tests for the backend Python code with pytest
- Runs linting with flake8 and black
- Runs tests for the frontend React code with Jest
- Runs linting with ESLint
- Builds the frontend application
- Uploads test coverage to Codecov

### 2. Deployment (`deploy.yml`)

This workflow handles the deployment of the application to the production environment when changes are pushed to the main branch.

This workflow:
- Builds the frontend application
- Configures Cloudinary integration
- Runs database migrations
- Deploys the application to the hosting provider
- Sends deployment status notifications

### 3. Cloudinary Setup (`cloudinary-setup.yml`)

This specialized workflow manages the Cloudinary configuration and setup for the application's media storage needs. It runs when changes are made to Cloudinary-related files or when manually triggered.

This workflow:
- Validates Cloudinary credentials
- Sets up required folders in the Cloudinary account
- Creates upload presets with appropriate settings
- Tests file upload functionality

## Setting Up GitHub Secrets

To use these workflows, you'll need to set up the following secrets in your GitHub repository:

### For CI/CD and Deployment
- `DATABASE_URL`: Connection string for your PostgreSQL database
- `SECRET_KEY`: Secret key for your Flask application
- `SLACK_WEBHOOK`: URL for posting deployment notifications to Slack
- `DEPLOY_KEY`: Key for authenticating with your deployment service

### For Cloudinary Integration
- `CLOUDINARY_CLOUD_NAME`: Your Cloudinary cloud name
- `CLOUDINARY_API_KEY`: Your Cloudinary API key
- `CLOUDINARY_API_SECRET`: Your Cloudinary API secret

## Local Development

When developing locally, you can use the following tools to ensure your code will pass the CI checks:

### Python (Backend)
```bash
# Install development dependencies
pip install flake8 black pytest pytest-cov

# Run linters
flake8 backend
black --check backend

# Run tests
cd backend
pytest --cov=.
```

### JavaScript (Frontend)
```bash
# Install dependencies
cd frontend
npm install

# Run linter
npm run lint

# Run tests
npm test
```

## Setting Up Cloudinary Locally

1. Sign up for a Cloudinary account at https://cloudinary.com/
2. Create a `.env` file in the backend directory with your Cloudinary credentials:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```
3. Install the Cloudinary Python SDK:
```bash
pip install cloudinary
```
4. Test your configuration:
```python
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure cloudinary
cloudinary.config(
    cloud_name=os.environ['CLOUDINARY_CLOUD_NAME'],
    api_key=os.environ['CLOUDINARY_API_KEY'],
    api_secret=os.environ['CLOUDINARY_API_SECRET'],
    secure=True
)

# Test connection
print(cloudinary.api.ping())
``` 