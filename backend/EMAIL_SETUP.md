# SmartProBono Email Setup

This document explains how to set up and configure the email functionality for SmartProBono.

## Environment Variables

To use the email features, you need to set the following environment variables:

```
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=noreply@smartprobono.org
EMAIL_FROM_NAME=SmartProBono
APP_URL=http://localhost:3000
```

## Using Gmail

If you're using Gmail, you'll need to:

1. Enable 2-Factor Authentication on your Google account
2. Generate an "App Password" specifically for SmartProBono
3. Use that App Password as the `EMAIL_PASSWORD`

## Email Templates

Email templates are stored in `backend/services/email_templates/`.

### Available Templates

1. `beta_confirmation.html` - Sent when a user signs up for the beta
2. `beta_welcome.html` - Sent when a user confirms their email

## API Endpoints

### Beta Signup

```
POST /api/beta/signup
{
  "email": "user@example.com",
  "source": "landing_page" (optional)
}
```

### Email Confirmation

```
GET /api/beta/confirm/{token}
```

### Email Subscription

```
POST /api/beta/subscribe
{
  "email": "user@example.com",
  "preferences": {
    "productUpdates": true,
    "legalNews": false,
    "tips": true
  }
}
```

## Database Migration

To add the necessary database fields for email subscriptions, run:

```
flask db upgrade
```

This will execute the migration in `migrations/add_subscription_fields.py` to add:

- `subscription_preferences` - JSON field to store preferences
- `subscribed_at` - Timestamp for when user subscribed
- `is_subscribed` - Boolean flag indicating subscription status

## Testing Email Functionality

You can test email sending without actually sending emails by:

1. Not setting `EMAIL_USERNAME` and `EMAIL_PASSWORD` in development
2. The email service will log the email content instead of sending it

## Troubleshooting

### Emails not sending

1. Check that your SMTP credentials are correct
2. Ensure your email provider allows SMTP access
3. If using Gmail, ensure you're using an App Password, not your regular password
4. Check the logs for any error messages

### Database migration issues

1. If you encounter database migration issues, you can manually add the columns:
   ```sql
   ALTER TABLE beta_signups ADD COLUMN subscription_preferences JSONB;
   ALTER TABLE beta_signups ADD COLUMN subscribed_at TIMESTAMP;
   ALTER TABLE beta_signups ADD COLUMN is_subscribed BOOLEAN DEFAULT false;
   ``` 