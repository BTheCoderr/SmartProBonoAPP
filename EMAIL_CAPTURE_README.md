# SmartProBono Email Capture System

## Overview

This document explains how the email signup system for SmartProBono works. The current implementation uses a simple file-based storage system for early beta signups, which can later be migrated to a more robust database solution.

## How It Works

1. **Signup Endpoint**: When a user submits their email on the beta landing page, the frontend sends a POST request to `/api/beta/signup` with the email address.

2. **Email Storage**: The API processes this request and:
   - Validates the email format
   - Logs the email to a file (`email_signups/all_signups.txt`)
   - Saves detailed signup information as JSON (`email_signups/user_at_domain.com.json`)
   - Simulates sending a confirmation email (in production, this would connect to an email service)

3. **Confirmation Response**: The API returns a JSON response confirming the signup was successful.

## Where Emails Are Stored

All beta signup emails are stored in the `email_signups/` directory:

- `all_signups.txt`: A CSV-style file with all email addresses and signup timestamps
- Individual JSON files for each signup (e.g., `user_at_domain.com.json`), containing:
  - Timestamp
  - Email address
  - Email subject
  - Email message content

## Accessing Signup Data

To view all signups, you can check:
```bash
cat email_signups/all_signups.txt
```

To view details for a specific signup:
```bash
cat email_signups/user_at_domain.com.json
```

## Production Implementation

For production, this system should be enhanced with:

1. **Database Storage**: Replace file storage with a proper database (PostgreSQL, MongoDB, etc.)
2. **Email Service Integration**: Connect to SendGrid, Mailgun, or a similar service to send actual emails
3. **Email Confirmation Flow**: Implement a proper double opt-in flow with confirmation links
4. **Admin Interface**: Create an admin dashboard to view and manage signups

## Migration Plan

When ready to move to production:

1. Extract all emails from `all_signups.txt`
2. Import them into your chosen email marketing platform or CRM
3. Set up proper segmentation for beta users
4. Create a welcome campaign for existing signups

## Security Considerations

The current implementation is for development/beta only. For production:

1. Implement proper data encryption
2. Set up backup procedures
3. Ensure compliance with privacy regulations (GDPR, CCPA, etc.)
4. Implement rate limiting to prevent abuse 