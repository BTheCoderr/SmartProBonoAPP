import React, { useRef, useState } from 'react';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import SignatureCanvas from 'react-signature-canvas';
import { PDFDocument } from 'pdf-lib';

const DigitalSignature = ({ pdfUrl, onSignComplete }) => {
  const [open, setOpen] = useState(false);
  const sigPad = useRef(null);
  const [signatureData, setSignatureData] = useState(null);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const clear = () => {
    sigPad.current.clear();
    setSignatureData(null);
  };

  const save = async () => {
    if (!sigPad.current.isEmpty()) {
      const signatureImage = sigPad.current.toDataURL();
      setSignatureData(signatureImage);

      try {
        // Load the PDF
        const existingPdfBytes = await fetch(pdfUrl).then(res => res.arrayBuffer());
        const pdfDoc = await PDFDocument.load(existingPdfBytes);
        const pages = pdfDoc.getPages();
        const firstPage = pages[0];

        // Convert signature to PNG
        const signatureBytes = await fetch(signatureImage).then(res => res.arrayBuffer());
        const signatureImage = await pdfDoc.embedPng(signatureBytes);

        // Add signature to PDF
        const { width, height } = firstPage.getSize();
        firstPage.drawImage(signatureImage, {
          x: 50,
          y: 50,
          width: 200,
          height: 50,
        });

        // Save the PDF
        const pdfBytes = await pdfDoc.save();
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });
        const signedPdfUrl = URL.createObjectURL(blob);

        onSignComplete(signedPdfUrl);
        handleClose();
      } catch (error) {
        console.error('Error adding signature to PDF:', error);
      }
    }
  };

  return (
    <>
      <Button variant="contained" color="primary" onClick={handleOpen}>
        Add Digital Signature
      </Button>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>Add Your Digital Signature</DialogTitle>
        <DialogContent>
          <Box sx={{ border: '1px solid #ccc', borderRadius: 1, my: 2 }}>
            <SignatureCanvas
              ref={sigPad}
              canvasProps={{
                width: 500,
                height: 200,
                className: 'signature-canvas',
                style: { width: '100%', height: '200px' }
              }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={clear}>Clear</Button>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={save} variant="contained" color="primary">
            Save Signature
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default DigitalSignature; 