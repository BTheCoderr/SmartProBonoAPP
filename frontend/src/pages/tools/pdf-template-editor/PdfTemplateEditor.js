import React, { useEffect, useRef } from "react";
import { Box, Typography, Paper } from "@mui/material";
// If types get in the way, keep the ts-ignore — @pdfme/ui ships JS
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { Designer } from "@pdfme/ui";
import { template as baseTemplate, fonts } from "../../../lib/pdf/pdfmeSchemas";

const PdfTemplateEditor = () => {
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current) return;

    const d = new Designer({
      domContainer: ref.current,
      template: baseTemplate,
      options: { font: fonts },
    });

    // You can call d.getTemplate() and d.setTemplate() via devtools to export/import templates.
    return () => {
      // Designer has no explicit dispose, but clear container on unmount
      if (ref.current) ref.current.innerHTML = "";
    };
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 2, fontWeight: 600 }}>
        SmartProBono PDF Template Editor
      </Typography>
      <Typography variant="body1" sx={{ mb: 3, color: 'text.secondary' }}>
        Drag fields, save template JSON in devtools with <code>d.getTemplate()</code>, then paste into <code>/lib/pdf/pdfmeSchemas.ts</code>.
      </Typography>
      <Paper 
        ref={ref} 
        sx={{ 
          height: "80vh", 
          border: "1px solid #e5e7eb", 
          borderRadius: 2,
          overflow: 'hidden'
        }} 
      />
    </Box>
  );
};

export default PdfTemplateEditor;
