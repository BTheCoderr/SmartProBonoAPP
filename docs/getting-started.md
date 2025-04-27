# Getting Started with SmartProBono

This guide will help you set up your development environment and get started with contributing to the SmartProBono project.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+** (for backend development)
- **Node.js 16+** and **npm** (for frontend development)
- **Git**
- **MongoDB** (for local database)
- **Redis** (for WebSocket pub/sub and caching)

## Clone the Repository

```bash
git clone https://github.com/your-organization/SmartProBono.git
cd SmartProBono
```

## Backend Setup

1. **Create a virtual environment**:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:

Create a `.env` file in the `backend` directory with the following:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
MONGODB_URI=mongodb://localhost:27017/smartprobono
JWT_SECRET_KEY=your_jwt_secret
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000
```

4. **Initialize the database**:

```bash
flask init-db
```

5. **Run the backend server**:

```bash
flask run
# Alternatively, to run with WebSocket support:
python app.py
```

The API server will be available at `http://localhost:5003`.

## Frontend Setup

1. **Install dependencies**:

```bash
cd frontend
npm install
```

2. **Set up environment variables**:

Create a `.env` file in the `frontend` directory with:

```
REACT_APP_API_URL=http://localhost:5003
REACT_APP_WEBSOCKET_URL=http://localhost:5003
```

3. **Run the development server**:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`.

## Project Structure

### Backend

- **`backend/app.py`**: Main Flask application entry point
- **`backend/routes/`**: API routes and blueprints
- **`backend/models/`**: Database models
- **`backend/services/`**: Business logic and services
- **`backend/websocket/`**: WebSocket implementation
- **`backend/utils/`**: Utility functions

### Frontend

- **`frontend/src/App.js`**: Main React component
- **`frontend/src/pages/`**: Page components
- **`frontend/src/components/`**: Reusable UI components
- **`frontend/src/services/`**: API and WebSocket services
- **`frontend/src/utils/`**: Utility functions
- **`frontend/src/context/`**: React context providers

## Key Features and Where to Find Them

1. **Authentication**: 
   - Backend: `backend/routes/auth.py`, `backend/utils/auth.py`
   - Frontend: `frontend/src/services/auth.js`, `frontend/src/context/AuthContext.js`

2. **Notifications System**:
   - Backend: `backend/websocket/services/notification_service.py`
   - Frontend: `frontend/src/components/Notifications/`

3. **Immigration Services**:
   - Backend: `backend/routes/immigration.py`
   - Frontend: `frontend/src/pages/Immigration/`

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your changes** and write tests.

3. **Run the linting tools**:
   - Backend: `flake8`
   - Frontend: `npm run lint`

4. **Commit your changes** using conventional commits:
   ```bash
   git commit -m "feat: add new notification feature"
   ```

5. **Push your branch** and create a pull request.

## WebSocket Development

The application uses Socket.IO for real-time features. When developing WebSocket features:

1. Make sure Redis is running locally.
2. Implement server-side event handlers in `backend/websocket/core.py`.
3. Add client-side listeners in `frontend/src/services/socket.js`.
4. Test your implementation using the WebSocket testing tools in the admin dashboard.

## Common Issues and Solutions

1. **WebSocket connection issues**: 
   - Ensure Redis is running
   - Check CORS configuration in `backend/app.py`

2. **Authentication problems**:
   - Verify JWT tokens in local storage
   - Check JWT expiration settings

3. **MongoDB connection errors**:
   - Verify MongoDB is running (`mongod`)
   - Check connection string in `.env`

## Additional Resources

- [WebSocket API Documentation](./websocket-api-documentation.md)
- [Notifications Implementation](./notifications-implementation-summary.md)
- [MVP Features & Roadmap](./mvp-features-roadmap.md)

## Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the existing documentation in the `docs/` directory
2. Reach out to the development team in our Slack channel
3. Create an issue in the GitHub repository 