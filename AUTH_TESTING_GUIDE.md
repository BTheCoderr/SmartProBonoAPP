# Authentication and Route Guards Testing Guide

This guide provides step-by-step instructions for manually testing the authentication flows and route guards in the SmartProBono application.

## Prerequisites

1. The frontend application is running (npm run start)
2. The backend API is running 
3. There is a test user available (you can create one through the registration page)

## Test Scenarios

### 1. Authentication Flow Testing

#### Registration
1. Navigate to `/register`
2. Fill in the registration form with valid details:
   - First Name: Test
   - Last Name: User
   - Email: test@example.com (use a unique email for each test)
   - Password: Test1234!
   - Confirm Password: Test1234!
3. Submit the form
4. Verify you are redirected to the dashboard
5. Verify JWT token is stored in localStorage

#### Login
1. Log out or open a new incognito window
2. Navigate to `/login`
3. Enter the credentials for a registered user
4. Submit the form
5. Verify you are redirected to the dashboard
6. Verify JWT token is stored in localStorage

#### Error Handling
1. Navigate to `/login`
2. Enter invalid credentials:
   - Email: test@example.com
   - Password: wrongpassword
3. Submit the form
4. Verify error message is displayed correctly
5. Try registration with an existing email
6. Verify error message is displayed correctly

### 2. Route Guards Testing

#### Protected Routes
1. Log out or clear localStorage
2. Try to navigate directly to the following URLs:
   - `/dashboard`
   - `/forms`
   - `/profile`
   - `/documents`
3. Verify you are redirected to the login page
4. Log in with valid credentials
5. Try accessing the protected routes again
6. Verify you can access the pages when authenticated

#### Role-Based Access
1. Log in with a non-admin user
2. Try to navigate to `/admin`
3. Verify you are redirected to the unauthorized page
4. Log out and log in with an admin user
5. Verify you can access the admin dashboard

#### Deep Nested Routes
1. Log out
2. Try to navigate to:
   - `/services/contracts`
   - `/resources/premium-guides`
3. Verify you are redirected to the login page
4. Log in with valid credentials
5. Verify you can access these routes

### 3. Token Management Testing

#### Token Expiration
1. Log in with valid credentials
2. Modify the JWT token expiration time (for testing purposes)
3. Wait for the token to expire
4. Try to access a protected route
5. Verify the system attempts to refresh the token
6. Verify you remain logged in if refresh is successful

#### Token Refresh
1. Log in with valid credentials
2. Inspect network requests when accessing protected routes after some time
3. Verify refresh token is used to obtain a new access token when needed

## Verification Steps

After completing the tests, ensure:

1. All routes that should be protected require authentication
2. Error messages are clear and informative
3. Redirections work properly (after login, user returns to the originally requested page)
4. Token refresh mechanism works correctly
5. Role-based access controls are enforced

## Common Issues

- JWT token not being stored in localStorage
- Missing Authorization header in API requests
- Improper handling of token expiration
- Unclear error messages for authentication failures
- Route guards not implemented consistently across all protected routes

## Documentation

Document any issues found during testing in the appropriate issue tracking system, including:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Browser and environment information 