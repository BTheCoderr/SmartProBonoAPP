# SmartProBono Split Deployment Setup

This document outlines the steps for setting up a split deployment with:
- Frontend hosted on Netlify (smartprobono.org)
- Backend hosted on Render (api.smartprobono.org)

## DNS Configuration

Add the following DNS records in your GoDaddy dashboard:

| Type  | Host/Name | Value/Target                   | TTL    |
|-------|-----------|--------------------------------|--------|
| CNAME | api       | smartprobonoapp.onrender.com   | 1 Hour |

Leave your existing records for the root domain (smartprobono.org) and www subdomain pointing to Netlify.

## Backend Setup (Render)

1. Your backend is already deployed on Render at: https://smartprobonoapp.onrender.com
2. In your Render dashboard, go to the backend service settings
3. Under "Custom Domains", add api.smartprobono.org as a custom domain
4. Verify domain ownership using the DNS verification process
5. Environment variables are already updated with the correct CORS settings

## Frontend Setup (Netlify)

1. Your frontend is already deployed on Netlify connected to smartprobono.org
2. The frontend code has been updated to use the api.smartprobono.org endpoint
3. No additional frontend changes are needed

## Testing the Setup

After DNS propagation (which can take up to 24 hours, but often happens much faster), verify that:

1. https://smartprobono.org still works correctly and shows your frontend
2. https://api.smartprobono.org is functioning as your backend
3. API calls from the frontend to the backend are working correctly

## Troubleshooting

If API calls are failing, check the following:

1. **CORS Issues**: Verify that the backend's CORS settings include both the main domain and the www subdomain
2. **DNS Propagation**: Use [DNSChecker](https://dnschecker.org) to verify your DNS records have propagated
3. **Backend Service**: Ensure the backend service is running properly on Render
4. **Frontend Config**: Double-check the `config.js` file to ensure all API URLs are correctly set

## Additional Notes

- The backend automatically handles CORS for requests from smartprobono.org and www.smartprobono.org
- The JWT authentication tokens and cookies will work across domains
- The websocket connections have been configured to use the api subdomain

If you need to add more domains in the future, update both:
1. The CORS settings in `backend/config.py`
2. The frontend configuration in `frontend/src/config.js` 