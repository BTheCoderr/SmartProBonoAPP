# Zoho Email Setup for SmartProBono Contact Form

## Your Current Setup
- ✅ **Domain**: smartprobono.org
- ✅ **Email**: bferrell@smartprobono.org (Zoho Mail Free)
- ✅ **Gmail**: bferrell514@gmail.com (for receiving contact form emails)
- ✅ **Backend**: Configured to send emails via Gmail SMTP
- ✅ **Forwarding**: Gmail → Zoho (manual or automatic)

## Zoho Mail Free Plan Limitations
The Zoho Mail Free plan has some limitations for SMTP:
- **SMTP Access**: Limited (may require paid plan for full SMTP)
- **API Access**: Limited
- **Daily Send Limits**: Lower limits than paid plans

## Setup Options

### Option 1: Gmail SMTP (Recommended - Working Solution)
Configure your backend to use Gmail's SMTP servers and forward to your professional email.

**Environment Variables:**
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=bferrell514@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=noreply@smartprobono.org
```

**Steps:**
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an "App Password" for SmartProBono
3. Set the app password as MAIL_PASSWORD
4. Emails will be sent to your Gmail inbox
5. Forward important emails to bferrell@smartprobono.org

### Option 2: Resend API (Alternative)
Use Resend to send emails FROM your domain TO your Gmail inbox.

**Environment Variables:**
```bash
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@smartprobono.org
```

**Steps:**
1. Use your existing Resend API key
2. Emails will be sent to bferrell514@gmail.com
3. Forward important emails to bferrell@smartprobono.org

### Option 3: Email Forwarding (Simplest)
Set up email forwarding in Zoho to forward `noreply@smartprobono.org` to your main email.

## Testing Your Setup

### Test 1: Gmail SMTP
```bash
# Set environment variables
export MAIL_SERVER=smtp.gmail.com
export MAIL_USERNAME=bferrell514@gmail.com
export MAIL_PASSWORD=your-gmail-app-password

# Test the configuration
python backend/test_email.py
```

### Test 2: Resend API
```bash
# Set environment variables
export RESEND_API_KEY=your-resend-key
export RESEND_FROM_EMAIL=noreply@smartprobono.org

# Test the configuration
python backend/test_email.py
```

## How It Will Work

### Contact Form Flow:
1. User fills out contact form on your website
2. Frontend sends data to `/api/contact/submit`
3. Backend sends email to `bferrell514@gmail.com`
4. Email appears in your Gmail inbox
5. You can forward important emails to `bferrell@smartprobono.org`
6. User receives auto-reply confirmation

### Email Content:
- **To**: bferrell514@gmail.com (your Gmail inbox)
- **From**: noreply@smartprobono.org (your domain)
- **Subject**: "New Contact Form Submission from [Name]"
- **Content**: User's message and contact details

## Troubleshooting

### If Zoho SMTP doesn't work:
- Check if SMTP is enabled in Zoho settings
- Try using app-specific password
- Consider upgrading to Zoho Mail paid plan
- Fall back to Resend option

### If Resend doesn't work:
- Verify domain in Resend dashboard
- Check DNS records are correct
- Ensure API key is valid

## Next Steps

1. **Try Zoho SMTP first** (free option)
2. **If that fails, use Resend** (more reliable)
3. **Test the contact form** with both options
4. **Choose the working solution** for production

## Cost Analysis

- **Zoho Mail Free**: $0/month (limited SMTP)
- **Zoho Mail Paid**: ~$1/month (full SMTP access)
- **Resend**: Free tier available, then ~$20/month

## Recommendation

For your setup, I recommend:
1. **Use Gmail SMTP** (reliable and free)
2. **Forward important emails** to your professional Zoho address
3. **Use Resend as backup** if Gmail has issues
4. **Professional email signature** included in template

The contact form will work perfectly - emails go to your Gmail first, then you can forward the important ones to your professional `bferrell@smartprobono.org` address!
