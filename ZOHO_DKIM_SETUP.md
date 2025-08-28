# Setting Up DKIM Authentication in Zoho for SmartProBono

This guide explains how to configure DKIM (DomainKeys Identified Mail) authentication for SmartProBono emails using Zoho Mail.

## What is DKIM?

DKIM is an email authentication method designed to detect email spoofing. It allows the receiver to check that an email claimed to have come from a specific domain was indeed authorized by the owner of that domain.

## Benefits of DKIM for SmartProBono

1. **Improved Deliverability**: Emails are less likely to be marked as spam
2. **Enhanced Security**: Reduces email spoofing and phishing attempts
3. **Builds Reputation**: Helps establish the domain's email sending reputation
4. **User Trust**: Recipients can trust emails are genuinely from your organization

## Setup Instructions

### Step 1: Access Zoho Mail Admin Console

1. Log in to the [Zoho Mail Admin Console](https://mailadmin.zoho.com)
2. Navigate to your domain (smartprobono.org)

### Step 2: Configure DKIM in Zoho

1. From the Admin Console, go to **Email Authentication**
2. Select the **DKIM** tab
3. Click on **Configure DKIM**
4. Choose **Domain Selector** (typically "zmail" is the default in Zoho)
5. Click **Save**

### Step 3: Add DKIM DNS Records

Zoho will generate a DKIM record that needs to be added to your domain's DNS settings:

1. Note the DKIM record that looks like:
   ```
   Selector: zmail
   Record Type: TXT
   Host: zmail._domainkey.smartprobono.org
   Value: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBA...
   ```

2. Go to your DNS provider (e.g., GoDaddy, Namecheap, AWS Route 53)
3. Add a new TXT record with:
   - **Host/Name**: `zmail._domainkey` (or your selected name)
   - **Value**: The entire string starting with `v=DKIM1...`
   - **TTL**: 3600 (or as recommended by your DNS provider)

### Step 4: Verify DKIM Configuration

1. Return to Zoho Mail Admin Console
2. Go to **Email Authentication** > **DKIM**
3. Click **Verify DKIM**
4. Wait for verification to complete (may take 24-48 hours for DNS propagation)

### Step 5: Test Email Delivery

Once DKIM is verified (as shown in your screenshot):

1. Run the SmartProBono API with email configuration:
   ```bash
   ./run_with_email.sh
   ```
2. Submit a test signup on your beta page
3. Check that the email arrives and isn't marked as spam
4. Verify the email headers to confirm DKIM is working properly

## Troubleshooting

If DKIM verification fails:

1. **DNS Propagation**: Allow 24-48 hours for DNS changes to propagate
2. **Record Format**: Ensure the TXT record doesn't have extra spaces or line breaks
3. **Selector Name**: Verify the selector name matches exactly between Zoho and DNS
4. **Value Formatting**: Some DNS providers have special requirements for long TXT records

## Additional Email Security Recommendations

For maximum email deliverability, also configure:

1. **SPF Record**: Specifies which mail servers are authorized to send email on behalf of your domain
2. **DMARC Record**: Tells receiving servers what to do if SPF or DKIM checks fail

## Getting Support

If you need assistance with your Zoho DKIM setup:

- Zoho Support: https://help.zoho.com/portal/en/home
- Email: support@zohomail.com 