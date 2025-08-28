const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');
const { createLogger } = require('../utils/logger');
const encryption = require('../utils/encryption');

const logger = createLogger('pdf-service');

class PDFService {
  constructor() {
    this.templatesPath = path.join(__dirname, '../templates/legal');
    this.outputPath = path.join(__dirname, '../generated');
    
    // Ensure output directory exists
    if (!fs.existsSync(this.outputPath)) {
      fs.mkdirSync(this.outputPath, { recursive: true });
    }
  }

  async generateLegalDocument(templateName, data, options = {}) {
    try {
      // Create a new PDF document
      const doc = new PDFDocument({
        size: 'LETTER',
        margins: {
          top: 72,
          bottom: 72,
          left: 72,
          right: 72
        },
        info: {
          Title: data.title || 'Legal Document',
          Author: 'SmartProBono',
          Subject: 'Legal Document',
          Keywords: 'legal,document,automated',
          CreationDate: new Date()
        }
      });

      // Set up the document
      this.setupDocument(doc, options);

      // Load and apply template
      const template = await this.loadTemplate(templateName);
      await this.applyTemplate(doc, template, data);

      // Generate unique filename
      const filename = `${templateName}-${Date.now()}.pdf`;
      const outputPath = path.join(this.outputPath, filename);

      // Create write stream
      const stream = fs.createWriteStream(outputPath);

      // Handle stream events
      await new Promise((resolve, reject) => {
        stream.on('finish', resolve);
        stream.on('error', reject);
        doc.pipe(stream);
        doc.end();
      });

      // Encrypt the document if specified
      if (options.encrypt) {
        await this.encryptDocument(outputPath);
      }

      logger.info(`Generated PDF document: ${filename}`);
      return {
        filename,
        path: outputPath,
        size: fs.statSync(outputPath).size
      };
    } catch (error) {
      logger.error('Error generating PDF:', error);
      throw new Error('Failed to generate PDF document');
    }
  }

  setupDocument(doc, options) {
    // Set default font
    doc.font('Helvetica');
    doc.fontSize(12);

    // Add letterhead if specified
    if (options.letterhead) {
      this.addLetterhead(doc, options.letterhead);
    }

    // Add watermark if specified
    if (options.watermark) {
      this.addWatermark(doc, options.watermark);
    }

    // Add header and footer if specified
    if (options.header) {
      this.addHeader(doc, options.header);
    }
    if (options.footer) {
      this.addFooter(doc, options.footer);
    }
  }

  async loadTemplate(templateName) {
    const templatePath = path.join(this.templatesPath, `${templateName}.json`);
    try {
      const template = require(templatePath);
      return template;
    } catch (error) {
      logger.error(`Error loading template ${templateName}:`, error);
      throw new Error(`Template ${templateName} not found`);
    }
  }

  async applyTemplate(doc, template, data) {
    // Apply template sections
    for (const section of template.sections) {
      switch (section.type) {
        case 'header':
          this.addSectionHeader(doc, section, data);
          break;
        case 'text':
          this.addText(doc, section, data);
          break;
        case 'table':
          this.addTable(doc, section, data);
          break;
        case 'signature':
          this.addSignatureBlock(doc, section, data);
          break;
        case 'list':
          this.addList(doc, section, data);
          break;
        case 'pageBreak':
          doc.addPage();
          break;
      }
    }
  }

  addSectionHeader(doc, section, data) {
    doc.fontSize(14)
       .font('Helvetica-Bold')
       .text(this.replaceVariables(section.content, data))
       .moveDown();
  }

  addText(doc, section, data) {
    doc.fontSize(12)
       .font('Helvetica')
       .text(this.replaceVariables(section.content, data))
       .moveDown();
  }

  addTable(doc, section, data) {
    const table = section.content.map(row => 
      row.map(cell => this.replaceVariables(cell, data))
    );

    const cellPadding = 10;
    const columnWidth = (doc.page.width - doc.page.margins.left - doc.page.margins.right) / table[0].length;

    table.forEach((row, rowIndex) => {
      const rowHeight = 20;
      const y = doc.y;

      row.forEach((cell, columnIndex) => {
        const x = doc.page.margins.left + (columnWidth * columnIndex);
        
        // Draw cell border
        doc.rect(x, y, columnWidth, rowHeight).stroke();
        
        // Add cell content
        doc.text(cell, 
          x + cellPadding, 
          y + cellPadding,
          {
            width: columnWidth - (cellPadding * 2),
            align: 'left'
          }
        );
      });

      doc.moveDown();
    });
  }

  addSignatureBlock(doc, section, data) {
    doc.moveDown(2);
    
    // Add signature line
    const lineWidth = 200;
    const lineY = doc.y + 20;
    doc.moveTo(doc.page.margins.left, lineY)
       .lineTo(doc.page.margins.left + lineWidth, lineY)
       .stroke();

    // Add signature labels
    doc.fontSize(10)
       .text('Signature', doc.page.margins.left, lineY + 5)
       .text('Date', doc.page.margins.left + lineWidth - 50, lineY + 5);

    doc.moveDown(2);
  }

  addList(doc, section, data) {
    const items = section.content.map(item => 
      this.replaceVariables(item, data)
    );

    items.forEach((item, index) => {
      doc.fontSize(12)
         .text(`${index + 1}. ${item}`)
         .moveDown(0.5);
    });
  }

  addLetterhead(doc, letterhead) {
    // Add logo if provided
    if (letterhead.logo) {
      doc.image(letterhead.logo, 50, 50, { width: 150 });
    }

    // Add company info
    doc.fontSize(10)
       .text(letterhead.companyName, { align: 'right' })
       .text(letterhead.address, { align: 'right' })
       .text(letterhead.contact, { align: 'right' })
       .moveDown(2);
  }

  addWatermark(doc, text) {
    const pages = doc.bufferedPageRange();
    for (let i = 0; i < pages.count; i++) {
      doc.switchToPage(i);
      
      doc.save()
         .rotate(45, { origin: [doc.page.width / 2, doc.page.height / 2] })
         .fontSize(60)
         .fillColor('grey', 0.3)
         .text(text, 0, doc.page.height / 2, {
           align: 'center'
         })
         .restore();
    }
  }

  addHeader(doc, headerText) {
    doc.on('pageAdded', () => {
      doc.fontSize(10)
         .text(headerText, doc.page.margins.left, 30, {
           align: 'center'
         });
    });
  }

  addFooter(doc, footerText) {
    doc.on('pageAdded', () => {
      doc.fontSize(10)
         .text(
           footerText,
           doc.page.margins.left,
           doc.page.height - 50,
           {
             align: 'center'
           }
         );
    });
  }

  replaceVariables(text, data) {
    return text.replace(/\{\{(\w+)\}\}/g, (match, variable) => {
      return data[variable] || match;
    });
  }

  async encryptDocument(filePath) {
    try {
      const fileContent = await fs.promises.readFile(filePath);
      const encrypted = await encryption.encrypt(fileContent);
      await fs.promises.writeFile(filePath + '.enc', JSON.stringify(encrypted));
      await fs.promises.unlink(filePath);
      return filePath + '.enc';
    } catch (error) {
      logger.error('Error encrypting document:', error);
      throw new Error('Failed to encrypt document');
    }
  }

  async decryptDocument(filePath) {
    try {
      const encryptedContent = require(filePath);
      const decrypted = await encryption.decrypt(encryptedContent);
      const outputPath = filePath.replace('.enc', '');
      await fs.promises.writeFile(outputPath, decrypted);
      return outputPath;
    } catch (error) {
      logger.error('Error decrypting document:', error);
      throw new Error('Failed to decrypt document');
    }
  }
}

// Export singleton instance
module.exports = new PDFService(); 