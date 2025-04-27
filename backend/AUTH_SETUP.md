# SmartProBono Authentication System

This document provides details about the authentication system implemented in SmartProBono, including setup instructions, features, and testing procedures.

## Features

The authentication system includes the following features:

- **User Registration and Login**: Secure user registration and login with password hashing
- **Email Verification**: Email verification for new accounts and email changes
- **Password Reset**: Secure password reset flow with expiring tokens
- **Rate Limiting**: Protection against brute force attacks
- **Session Management**: Multi-device logout support and session tracking
- **JWT-based Authentication**: Secure, stateless authentication with JSON Web Tokens
- **Role-based Authorization**: Support for different user roles (client, lawyer, admin)
- **Security Notifications**: Email alerts for account activities like logins and password changes
- **Admin Dashboard**: User management and statistics for administrators

## Setup Instructions

### 1. Database Setup

The authentication system requires several fields in the User model. Run the migration script to add these fields:

```bash
cd backend
python migrations/add_auth_fields.py
```

### 2. Email Configuration

For email verification and password reset functionality, configure email settings in your `.env` file:

```bash
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_FROM=noreply@smartprobono.example.com
EMAIL_FROM_NAME=SmartProBono
APP_URL=http://localhost:3000
```

For Gmail, you'll need to set up an App Password in your Google Account settings.

### 3. JWT Secret Key

Set a strong JWT secret key in your `.env` file for production:

```bash
JWT_SECRET_KEY=your_secure_random_secret_key
```

In development, a random key will be generated automatically if not provided.

## Testing the Authentication System

Run the authentication tests to verify the system is working correctly:

```bash
cd backend
python run_auth_tests.py
```

This will execute a comprehensive suite of tests covering:
- User registration
- Login
- Token validation
- Profile updates
- Password reset flow
- Session management

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/register`: Register a new user
- `GET /api/auth/verify-email/<token>`: Verify email address
- `POST /api/auth/login`: Authenticate and receive JWT token
- `POST /api/auth/logout`: Logout current session
- `POST /api/auth/logout-all`: Logout from all devices
- `GET /api/auth/me`: Get current user profile
- `GET /api/auth/validate-token`: Validate JWT token
- `PUT /api/auth/update`: Update user profile
- `POST /api/auth/forgot-password`: Request password reset
- `POST /api/auth/reset-password`: Reset password with token

### Admin Endpoints

- `GET /api/admin/users`: List all users (paginated)
- `GET /api/admin/users/<user_id>`: Get specific user
- `PUT /api/admin/users/<user_id>`: Update user
- `DELETE /api/admin/users/<user_id>`: Delete user
- `GET /api/admin/stats`: Get user statistics

## Security Considerations

1. **Password Storage**: Passwords are hashed using Werkzeug's security utilities, which use PBKDF2 with SHA-256.
2. **Rate Limiting**: The system limits login attempts to prevent brute force attacks.
3. **Token Expiration**: JWT tokens expire after 24 hours by default.
4. **Email Verification**: Accounts require email verification before full access.
5. **Session Tracking**: All user sessions are tracked for multi-device management.
6. **Security Notifications**: Users receive emails for login attempts and password changes.

## Frontend Integration

The authentication system is designed to work with the existing React frontend. The frontend should:

1. Store JWT tokens in local storage or cookies
2. Include the token in Authorization headers for API requests
3. Handle token expiration gracefully
4. Redirect users to verification pages when needed

## Troubleshooting

### Common Issues

1. **Email sending fails**: Check your email provider settings and ensure you've set up the correct app password.
2. **Rate limiting too restrictive**: Adjust the rate limits in `routes/auth.py` if needed.
3. **JWT token issues**: Verify the `JWT_SECRET_KEY` is consistent across deployments.

For any other issues, check the application logs for detailed error messages. 