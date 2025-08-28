const express = require('express');
const PDFDocument = require('pdfkit');
const router = express.Router();

router.post('/generate-pdf', async (req, res) => {
  console.log('Received PDF generation request');
  console.log('Request body:', req.body);
  
  try {
    const { firstName, lastName, email, phone, message } = req.body;
    console.log('Processing data for:', firstName, lastName);
    
    // Prevent caching
    res.set({
      'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
      'Surrogate-Control': 'no-store'
    });
    
    // Log the extracted data
    console.log('Extracted data:', { firstName, lastName, email, phone, message });
    
    // Create a new PDF document
    const doc = new PDFDocument();
    
    // Set response headers
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename=contract.pdf`);
    
    // Pipe the PDF document to the response
    doc.pipe(res);
    
    // Add content to the PDF
    doc
      .fontSize(24)
      .text('Contract Document', { align: 'center' })
      .moveDown(2);
    
    // Add form data
    doc
      .fontSize(12)
      .text(`Client Information:`, { underline: true })
      .moveDown()
      .text(`Full Name: ${firstName} ${lastName}`)
      .moveDown()
      .text(`Email: ${email}`)
      .moveDown();
    
    if (phone) {
      doc.text(`Phone: ${phone}`).moveDown();
    }
    
    doc
      .moveDown()
      .text('Client Message:', { underline: true })
      .moveDown()
      .text(message, {
        width: 500,
        align: 'left'
      })
      .moveDown(2);
    
    // Add timestamp
    doc
      .text(`Document generated: ${new Date().toLocaleString()}`, {
        align: 'right',
        fontSize: 10
      });
    
    // Finalize the PDF
    doc.end();
    
  } catch (error) {
    console.error('PDF Generation Error:', error);
    res.status(500).json({ error: 'Failed to generate PDF', details: error.message });
  }
});

module.exports = router;