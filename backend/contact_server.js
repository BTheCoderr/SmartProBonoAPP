const express = require('express');
const cors = require('cors');
const https = require('https');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Resend API configuration
const RESEND_API_KEY = process.env.RESEND_API_KEY || 're_N7YNzBXp_HyNzVsWjuLNqxqUQr8oxaxvf';
const RESEND_URL = 'https://api.resend.com/emails';

// Health check endpoint
app.get('/api/contact/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'contact',
    message: 'Contact service is running'
  });
});

// Contact form submission endpoint
app.post('/api/contact/submit', async (req, res) => {
  try {
    const data = req.body;
    
    if (!data) {
      return res.status(400).json({ error: 'No data provided' });
    }
    
    // Validate required fields
    const requiredFields = ['firstName', 'lastName', 'email', 'message'];
    for (const field of requiredFields) {
      if (!data[field]) {
        return res.status(400).json({ error: `Missing required field: ${field}` });
      }
    }
    
    // Send contact form email
    const success = await sendContactEmail(data);
    
    if (success) {
      // Send auto-reply
      await sendAutoReply(data.email, `${data.firstName} ${data.lastName}`);
      
      res.json({
        success: true,
        message: 'Contact form submitted successfully. We will get back to you within 24 hours.'
      });
    } else {
      res.status(500).json({
        success: false,
        error: 'Failed to send contact form. Please try again later.'
      });
    }
    
  } catch (error) {
    console.error('Error processing contact form:', error);
    res.status(500).json({
      success: false,
      error: 'An error occurred while processing your request.'
    });
  }
});

async function sendContactEmail(formData) {
  try {
    const payload = {
      from: 'SmartProBono <onboarding@resend.dev>',
      to: ['bferrell514@gmail.com'],
      subject: `New Contact Form Submission from ${formData.firstName} ${formData.lastName}`,
      html: `
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0F3D5E;">New Contact Form Submission</h2>
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <p><strong>Name:</strong> ${formData.firstName} ${formData.lastName}</p>
              <p><strong>Email:</strong> ${formData.email}</p>
              <p><strong>Phone:</strong> ${formData.phone || 'N/A'}</p>
            </div>
            <div style="background: #fff; padding: 20px; border-left: 4px solid #1FB6A6;">
              <h3 style="color: #0F3D5E; margin-top: 0;">Message:</h3>
              <p style="white-space: pre-wrap;">${formData.message}</p>
            </div>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="color: #666; font-size: 12px;">
              This message was sent from the SmartProBono contact form.
            </p>
          </div>
        </body>
        </html>
      `,
      text: `
New contact form submission received:

Name: ${formData.firstName} ${formData.lastName}
Email: ${formData.email}
Phone: ${formData.phone || 'N/A'}

Message:
${formData.message}

---
This message was sent from the SmartProBono contact form.
      `
    };
    
    const response = await new Promise((resolve, reject) => {
      const req = https.request(RESEND_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve({ status: res.statusCode, data }));
      });
      
      req.on('error', reject);
      req.write(JSON.stringify(payload));
      req.end();
    });
    
    if (response.status >= 200 && response.status < 300) {
      console.log('Contact form email sent successfully');
      return true;
    } else {
      console.error('Resend API error:', response.status, response.data);
      return false;
    }
    
  } catch (error) {
    console.error('Error sending contact form email:', error);
    return false;
  }
}

async function sendAutoReply(recipientEmail, recipientName) {
  try {
    const payload = {
      from: 'SmartProBono <onboarding@resend.dev>',
      to: [recipientEmail],
      subject: 'Thank you for contacting SmartProBono',
      html: `
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #0F3D5E;">Thank you for contacting SmartProBono!</h2>
            <p>Dear ${recipientName},</p>
            <p>Thank you for reaching out to SmartProBono! We have received your message and will get back to you within 24 hours.</p>
            <p>Your message is important to us, and we're here to help with your legal needs.</p>
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #0F3D5E; margin-top: 0;">Best regards,</h3>
              <p>The SmartProBono Team</p>
            </div>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="color: #666; font-size: 12px;">
              <strong>SmartProBono - Making Legal Help Accessible</strong><br>
              Email: bferrell@smartprobono.org<br>
              Phone: (401) 217-9799
            </p>
          </div>
        </body>
        </html>
      `,
      text: `
Dear ${recipientName},

Thank you for reaching out to SmartProBono! We have received your message and will get back to you within 24 hours.

Your message is important to us, and we're here to help with your legal needs.

Best regards,
The SmartProBono Team

---
SmartProBono - Making Legal Help Accessible
Email: bferrell@smartprobono.org
Phone: (401) 217-9799
      `
    };
    
    const response = await new Promise((resolve, reject) => {
      const req = https.request(RESEND_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve({ status: res.statusCode, data }));
      });
      
      req.on('error', reject);
      req.write(JSON.stringify(payload));
      req.end();
    });
    
    if (response.status >= 200 && response.status < 300) {
      console.log(`Auto-reply sent successfully to ${recipientEmail}`);
      return true;
    } else {
      console.error('Resend API error for auto-reply:', response.status, response.data);
      return false;
    }
    
  } catch (error) {
    console.error('Error sending auto-reply:', error);
    return false;
  }
}

app.listen(port, '0.0.0.0', () => {
  console.log(`🚀 Contact server running on http://localhost:${port}`);
  console.log(`📧 Email system ready - sending to bferrell514@gmail.com`);
});
