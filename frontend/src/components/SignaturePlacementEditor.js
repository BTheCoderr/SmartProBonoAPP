import React, { useEffect, useRef, useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';
import 'pdfjs-dist/web/pdf_viewer.css';
import {
  Box,
  Button,
  Typography,
  Card,
  CardContent,
  Stack,
  Alert,
} from '@mui/material';
import { Save as SaveIcon } from '@mui/icons-material';

// Set up PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

const SignaturePlacementEditor = ({ 
  pdfUrl, 
  initial, 
  onSave,
  templateName = 'default-template'
}) => {
  const canvasRef = useRef(null);
  const wrapperRef = useRef(null);
  const [scale, setScale] = useState(1);
  const [pageSize, setPageSize] = useState(null);
  const [boxes, setBoxes] = useState([
    {
      id: "client",
      x: initial?.client?.x ?? 380,
      y: initial?.client?.y ?? 120,
      w: initial?.client?.w ?? 160,
      h: initial?.client?.h ?? 60,
      label: "Client",
    },
    {
      id: "attorney",
      x: initial?.attorney?.x ?? 380,
      y: initial?.attorney?.y ?? 60,
      w: initial?.attorney?.w ?? 160,
      h: initial?.attorney?.h ?? 60,
      label: "Attorney",
    },
  ]);
  const [active, setActive] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const dragState = useRef(null);

  const clampBox = (b, size) => {
    if (!size) return b;
    const nx = Math.min(Math.max(0, b.x), size.w - b.w);
    const ny = Math.min(Math.max(0, b.y), size.h - b.h);
    return { ...b, x: nx, y: ny };
  };

  // Render page 1
  useEffect(() => {
    if (!pdfUrl) return;
    
    const loadPdf = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const loadingTask = await pdfjsLib.getDocument(pdfUrl).promise;
        const page = await loadingTask.getPage(1);
        const viewport = page.getViewport({ scale: 1 });
        
        // Fit width to ~800px
        const targetWidth = 800;
        const s = targetWidth / viewport.width;
        const scaled = page.getViewport({ scale: s });
        
        setScale(s);
        setPageSize({ w: scaled.width, h: scaled.height });
        
        const canvas = canvasRef.current;
        if (!canvas) return;
        
        const ctx = canvas.getContext("2d");
        canvas.width = Math.floor(scaled.width);
        canvas.height = Math.floor(scaled.height);
        
        await page.render({ canvasContext: ctx, viewport: scaled }).promise;
      } catch (err) {
        console.error('PDF loading error:', err);
        setError('Failed to load PDF. Please check the URL.');
      } finally {
        setLoading(false);
      }
    };

    loadPdf();
  }, [pdfUrl]);

  const onMouseDown = (e, id, mode) => {
    e.stopPropagation();
    setActive(id);
    const target = boxes.find(b => b.id === id);
    if (!target) return;
    
    dragState.current = { 
      dx: target.x, 
      dy: target.y, 
      mode, 
      startX: e.clientX, 
      startY: e.clientY 
    };
  };

  const onMouseMove = (e) => {
    if (!dragState.current || !active) return;
    
    const st = dragState.current;
    setBoxes(prev => prev.map(b => {
      if (b.id !== active) return b;
      
      if (st.mode === "move") {
        const nx = st.dx + (e.clientX - st.startX);
        const ny = st.dy - (e.clientY - st.startY) * -1; // Keep intuitive drag
        return clampBox({ ...b, x: nx, y: ny }, pageSize);
      } else {
        const newW = Math.max(40, b.w + (e.clientX - st.startX));
        const newH = Math.max(24, b.h + (e.clientY - st.startY));
        return clampBox({ ...b, w: newW, h: newH }, pageSize);
      }
    }));
  };

  const onMouseUp = () => {
    dragState.current = null;
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Convert canvas pixels to PDF points
      const toPdfUnits = (n) => Math.round((n / scale) * 1000) / 1000;

      const placements = {};
      for (const b of boxes) {
        placements[b.id] = {
          pageIndex: 0,
          x: toPdfUnits(b.x),
          y: toPdfUnits(b.y),
          width: toPdfUnits(b.w),
          height: toPdfUnits(b.h),
          label: b.label,
        };
      }

      // Save to Supabase
      const response = await fetch('/api/templates/save-placements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          templateName, 
          placements 
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save placements');
      }

      setSuccess(true);
      onSave?.(placements);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error('Save error:', err);
      setError(err.message || 'Failed to save placements');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !pageSize) {
    return (
      <Card>
        <CardContent>
          <Typography>Loading PDF...</Typography>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">{error}</Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Signature Placement Editor
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Drag the signature boxes to position them on the PDF. Resize using the bottom-right handle.
        </Typography>

        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={loading}
            sx={{
              backgroundColor: '#1565C0',
              '&:hover': {
                backgroundColor: '#0D47A1',
              },
            }}
          >
            {loading ? 'Saving...' : 'Save Placements'}
          </Button>
          
          {pageSize && (
            <Typography variant="body2" color="text.secondary">
              Page: {Math.round(pageSize.w)} × {Math.round(pageSize.h)} px @ scale {scale.toFixed(2)}
            </Typography>
          )}
        </Stack>

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Placements saved successfully!
          </Alert>
        )}

        <Box
          ref={wrapperRef}
          sx={{
            position: 'relative',
            display: 'inline-block',
            lineHeight: 0,
            border: '1px solid #e0e0e0',
            borderRadius: 1,
            overflow: 'hidden',
          }}
          onMouseMove={onMouseMove}
          onMouseUp={onMouseUp}
          onMouseLeave={onMouseUp}
        >
          <canvas
            ref={canvasRef}
            style={{ display: 'block' }}
          />
          
          {pageSize && boxes.map(box => (
            <Box
              key={box.id}
              sx={{
                position: 'absolute',
                border: `2px solid ${active === box.id ? '#1565C0' : '#1976D2'}`,
                borderRadius: 1,
                backgroundColor: 'rgba(25, 118, 210, 0.1)',
                cursor: 'move',
                userSelect: 'none',
                left: box.x,
                top: pageSize.h - box.y - box.h, // Flip Y coordinate
                width: box.w,
                height: box.h,
                '&:hover': {
                  backgroundColor: 'rgba(25, 118, 210, 0.2)',
                },
              }}
              onMouseDown={(e) => onMouseDown(e, box.id, "move")}
            >
              {/* Label */}
              <Typography
                variant="caption"
                sx={{
                  position: 'absolute',
                  top: -24,
                  left: 0,
                  backgroundColor: 'white',
                  px: 0.5,
                  borderRadius: 0.5,
                  boxShadow: 1,
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: '#1565C0',
                }}
              >
                {box.label}
              </Typography>
              
              {/* Resize handle */}
              <Box
                sx={{
                  position: 'absolute',
                  bottom: 0,
                  right: 0,
                  width: 16,
                  height: 16,
                  backgroundColor: '#1565C0',
                  cursor: 'se-resize',
                  borderRadius: '0 0 4px 0',
                  '&:hover': {
                    backgroundColor: '#0D47A1',
                  },
                }}
                onMouseDown={(e) => onMouseDown(e, box.id, "resize")}
              />
            </Box>
          ))}
        </Box>

        <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
          Drag the boxes to position signatures. Resize with the bottom-right handle. 
          Click "Save Placements" to store the coordinates for this template.
        </Typography>
      </CardContent>
    </Card>
  );
};

export default SignaturePlacementEditor;
