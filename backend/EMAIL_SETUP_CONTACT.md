# Contact Form Email Setup

## Overview
The contact form is now connected to a backend email service that can send real emails when properly configured.

## Current Status
- ✅ **Backend Email Service**: Created and functional
- ✅ **Contact Form Endpoint**: `/api/contact/submit` 
- ✅ **Frontend Integration**: Contact form now sends data to backend
- ⚠️ **Email Configuration**: Needs to be set up for actual email sending

## How It Works

### Without Email Configuration (Current State)
- Contact form submissions are logged to the backend console
- Users still see success message
- No actual emails are sent
- Perfect for development/testing

### With Email Configuration (Production Ready)
- Contact form submissions send real emails to `bferrell@smartprobono.org`
- Auto-reply emails are sent to users
- Full email functionality enabled

## Email Configuration

### Option 1: Resend API (Recommended)
To enable real email sending via Resend, set these environment variables:

```bash
# Resend API Configuration
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@smartprobono.org
```

### Option 2: SMTP (Alternative)
For traditional SMTP email sending:

```bash
# SMTP Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@smartprobono.org
```

### Resend Setup (Recommended)
1. Go to [resend.com](https://resend.com) and sign in with your account
2. Navigate to "API Keys" in the sidebar
3. Create a new API key
4. Copy the API key and set it as `RESEND_API_KEY`
5. The system will automatically send emails to `bferrell514@gmail.com`

### Gmail Setup (Alternative)
1. Enable 2-Factor Authentication on your Google account
2. Generate an "App Password" specifically for SmartProBono
3. Use that App Password as the `MAIL_PASSWORD`

### Other Email Providers
- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's SMTP settings

## Testing the Contact Form

### Development Mode (No Email Setup)
1. Fill out the contact form
2. Submit the form
3. Check the backend console logs for the email content
4. User sees success message

### Production Mode (With Email Setup)
1. Fill out the contact form
2. Submit the form
3. Email is sent to `bferrell@smartprobono.org`
4. Auto-reply is sent to the user
5. User sees success message

## API Endpoints

### POST `/api/contact/submit`
Submit contact form data.

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Doe", 
  "email": "john@example.com",
  "phone": "555-1234",
  "message": "Hello, I need help with..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Contact form submitted successfully. We will get back to you within 24 hours."
}
```

### GET `/api/contact/health`
Health check for contact service.

## Files Created/Modified

### Backend
- `backend/services/email_service.py` - Email service implementation
- `backend/routes/contact.py` - Contact form API endpoint
- `backend/routes/__init__.py` - Registered contact blueprint

### Frontend  
- `frontend/src/pages/Contact.js` - Updated to send data to backend

## Next Steps

1. **For Development**: No action needed - contact form works with logging
2. **For Production**: Set up email environment variables
3. **Optional**: Add email templates for better formatting
4. **Optional**: Add email validation and spam protection
