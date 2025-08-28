# SmartProBono Manual Test Checklist

This document provides a manual test checklist to verify all critical functionality before deployment.

## 1. User Authentication

- [ ] **Registration**
  - [ ] Navigate to `/register`
  - [ ] Fill in all required fields with valid information
  - [ ] Submit the form and verify you're redirected to login
  - [ ] Check for confirmation message/email (if enabled)

- [ ] **Login**
  - [ ] Navigate to `/login`
  - [ ] Enter the credentials created during registration
  - [ ] Submit the form and verify you're redirected to dashboard
  - [ ] Verify authentication-specific UI elements appear (username, logout button, etc.)

- [ ] **JWT Token Management**
  - [ ] Login and inspect browser local storage to verify JWT token is stored
  - [ ] Wait until token expiration (if set to a short time for testing)
  - [ ] Verify automatic token refresh or re-authentication prompt
  - [ ] Verify protected routes can't be accessed without a valid token

- [ ] **Logout**
  - [ ] Click logout button
  - [ ] Verify redirection to login page
  - [ ] Verify JWT token is removed from storage
  - [ ] Verify you cannot access protected routes after logging out

## 2. Document Management

- [ ] **Document Upload**
  - [ ] Navigate to documents section
  - [ ] Click "Upload" button
  - [ ] Select a valid document (PDF, DOCX, etc.)
  - [ ] Add metadata (title, description)
  - [ ] Submit and verify document appears in the list

- [ ] **Document Download**
  - [ ] In the documents list, find your uploaded document
  - [ ] Click download/view button
  - [ ] Verify document downloads or opens correctly
  - [ ] Verify document content matches the uploaded file

- [ ] **Document Templates**
  - [ ] Navigate to templates section
  - [ ] Create a new template with variables (e.g., `${name}`, `${date}`)
  - [ ] Save template and verify it appears in the list
  - [ ] Generate a document from template by filling in variables
  - [ ] Verify the generated document has the variables replaced with actual values

- [ ] **Document Search and Filtering**
  - [ ] With multiple documents uploaded, use the search function
  - [ ] Verify search results match the query
  - [ ] Use filters (by document type, date, etc.)
  - [ ] Verify filtered results match the selected criteria

## 3. Form Submission Workflow

- [ ] **Form Creation and Drafts**
  - [ ] Navigate to forms section
  - [ ] Start a new form (e.g., client intake form)
  - [ ] Fill out part of the form and save as draft
  - [ ] Verify form is saved and can be resumed later
  - [ ] Resume the draft form and complete remaining fields

- [ ] **Form Submission**
  - [ ] Submit a completed form
  - [ ] Verify submission confirmation is displayed
  - [ ] Verify form appears in the "Submitted Forms" list
  - [ ] Verify form data is correctly stored and displayed

- [ ] **Form Validation**
  - [ ] Attempt to submit a form with missing required fields
  - [ ] Verify appropriate error messages are displayed
  - [ ] Attempt to submit a form with invalid data
  - [ ] Verify validation messages appear and prevent submission

- [ ] **Form Review and Processing**
  - [ ] Login as an attorney/admin user
  - [ ] Navigate to forms queue/review section
  - [ ] View submitted form details
  - [ ] Change form status (approve/reject/request more info)
  - [ ] Verify status change is reflected in both admin and client views

## 4. Core Navigation Flows

- [ ] **Client User Navigation**
  - [ ] Login as a client
  - [ ] Verify access to dashboard, profile, documents, and forms
  - [ ] Verify no access to attorney-only or admin-only sections
  - [ ] Verify all client-specific UI elements are correctly displayed

- [ ] **Attorney User Navigation**
  - [ ] Login as an attorney
  - [ ] Verify access to case management, client lists, and templates
  - [ ] Verify document generation and form review capabilities
  - [ ] Verify attorney-specific UI elements and workflows

- [ ] **Admin User Navigation**
  - [ ] Login as an administrator
  - [ ] Verify access to user management and system settings
  - [ ] Test creating/modifying user accounts
  - [ ] Verify admin-specific features and analytics

- [ ] **Responsive Design**
  - [ ] Test all core navigation flows on a mobile device or using responsive design tools
  - [ ] Verify menus, forms, and content display correctly at different screen sizes
  - [ ] Test touch interactions on mobile devices

## 5. Email Functionality

- [ ] **User Registration Email**
  - [ ] Register a new account
  - [ ] Verify welcome email is sent to the registered address
  - [ ] Check email content and formatting

- [ ] **Password Reset Email**
  - [ ] Request password reset
  - [ ] Verify reset email is sent
  - [ ] Use reset link in email to reset password
  - [ ] Verify new password works

- [ ] **Document Sharing Email**
  - [ ] Share a document via email
  - [ ] Verify recipient receives email with correct document information
  - [ ] Test document access link in email

- [ ] **Form Submission Confirmation Email**
  - [ ] Submit a form
  - [ ] Verify confirmation email is sent
  - [ ] Check email for correct form reference and status information

## 6. Deployment-Ready Checks

- [ ] **Environment Variables**
  - [ ] Verify all required environment variables are set
  - [ ] Test with production configuration
  - [ ] Verify email server, database, and third-party service connections

- [ ] **Error Handling**
  - [ ] Test error scenarios (invalid input, server errors, etc.)
  - [ ] Verify user-friendly error messages are displayed
  - [ ] Check for proper logging of errors

- [ ] **Performance**
  - [ ] Test loading times for key pages
  - [ ] Verify document upload/download speeds are acceptable
  - [ ] Check form submission performance with large forms

- [ ] **Security**
  - [ ] Verify SSL/TLS configuration (for production)
  - [ ] Test CORS settings
  - [ ] Check for secure cookie settings
  - [ ] Verify rate limiting on authentication endpoints

## Test Completion

**Date Tested:** _________________

**Tested By:** _________________

**Notes:**

_________________________________________________

_________________________________________________

_________________________________________________ 