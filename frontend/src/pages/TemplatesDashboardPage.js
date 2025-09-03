import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Stack,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Chip,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
} from '@mui/material';
import { 
  PageLayout, 
  Section, 
  designTokens 
} from '../design-system';
import { 
  Save as SaveIcon, 
  Upload as UploadIcon, 
  GetApp as DownloadIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';

const TemplatesDashboardPage = () => {
  const [templates, setTemplates] = useState([]);
  const [selected, setSelected] = useState('');
  const [templateJson, setTemplateJson] = useState('');
  const [placements, setPlacements] = useState(null);
  const [generateResult, setGenerateResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const fileRef = useRef(null);

  const selectedRow = useMemo(
    () => templates.find(t => t.template_name === selected),
    [templates, selected]
  );

  const loadTemplates = async () => {
    try {
      const res = await fetch('/api/templates/list');
      const json = await res.json();
      if (json?.items) {
        setTemplates(json.items);
      }
    } catch (err) {
      console.error('Error loading templates:', err);
      setError('Failed to load templates');
    }
  };

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplate = async (name) => {
    try {
      setSelected(name);
      setGenerateResult(null);
      setError(null);

      // Load template JSON
      const t = await fetch(`/api/templates/get?templateName=${encodeURIComponent(name)}`).then(r => r.json());
      if (t?.template?.template_json) {
        setTemplateJson(JSON.stringify(t.template.template_json, null, 2));
      } else {
        setTemplateJson('{\n  "basePdf": null,\n  "schemas": []\n}');
      }

      // Load placements
      const p = await fetch(`/api/templates/placements?templateName=${encodeURIComponent(name)}`).then(r => r.json());
      setPlacements(p?.placements || null);
    } catch (err) {
      console.error('Error loading template:', err);
      setError('Failed to load template');
    }
  };

  const handleSaveTemplate = async () => {
    try {
      setBusy(true);
      setError(null);
      
      const templateName = selected || prompt('Template name?') || '';
      if (!templateName) {
        setError('Template name is required');
        return;
      }

      const payload = {
        templateName,
        templateJson: JSON.parse(templateJson || '{}'),
      };

      const res = await fetch('/api/templates/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json();
        if (res.status === 401) {
          setError('Please log in to save templates');
          return;
        }
        throw new Error(errorData.error || 'Save failed');
      }

      setSuccess('Template saved successfully');
      await loadTemplates();
      if (!selected) setSelected(templateName);
      
      setTimeout(() => setSuccess(null), 3000);
    } catch (e) {
      console.error('Save error:', e);
      setError(e?.message || 'Save failed');
    } finally {
      setBusy(false);
    }
  };

  const handleSavePlacements = async () => {
    try {
      setBusy(true);
      setError(null);
      
      const name = selected || prompt('Template name?') || '';
      if (!name) {
        setError('Template name is required');
        return;
      }

      const obj = placements || {};
      const res = await fetch('/api/templates/save-placements', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ templateName: name, placements: obj }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        if (res.status === 401) {
          setError('Please log in to save placements');
          return;
        }
        throw new Error(errorData.error || 'Save placements failed');
      }

      setSuccess('Placements saved successfully');
      setTimeout(() => setSuccess(null), 3000);
    } catch (e) {
      console.error('Save placements error:', e);
      setError(e?.message || 'Save placements failed');
    } finally {
      setBusy(false);
    }
  };

  const handleUploadBasePdf = async () => {
    try {
      setBusy(true);
      setError(null);
      
      const name = selected || prompt('Template name?') || '';
      if (!name) {
        setError('Template name is required');
        return;
      }

      const file = fileRef.current?.files?.[0];
      if (!file) {
        setError('Choose a PDF file first');
        return;
      }

      const form = new FormData();
      form.append('file', file);
      form.append('templateName', name);

      const res = await fetch('/api/templates/upload-base', { 
        method: 'POST', 
        body: form 
      });
      
      const json = await res.json();
      if (!res.ok) {
        if (res.status === 401) {
          setError('Please log in to upload files');
          return;
        }
        throw new Error(json?.error || 'Upload failed');
      }

      setSuccess('Base PDF uploaded successfully');
      await loadTemplates();
      setTimeout(() => setSuccess(null), 3000);
    } catch (e) {
      console.error('Upload error:', e);
      setError(e?.message || 'Upload failed');
    } finally {
      setBusy(false);
    }
  };

  const handleGenerateTest = async () => {
    try {
      setBusy(true);
      setError(null);
      
      const name = selected || (templates[0]?.template_name || '');
      if (!name) {
        setError('No template selected');
        return;
      }

      const payload = {
        caseNumber: `SPB-DEMO-${Math.floor(Math.random() * 100000)}`,
        templateName: name,
        includeSignature: true,
        clientSignature: { type: 'image' },
        attorneySignature: { type: 'typed', text: 'A. Rivera, Esq.' },
        bodyText: 'Generated from Templates Dashboard test',
        tableRows: [
          { cols: ['Document', 'Status', 'Notes'] },
          { cols: ['Intake Form', 'Prepared', 'Pending review'] },
          { cols: ['Fee Waiver', 'Queued', 'Waiting for signature'] },
        ],
      };

      const res = await fetch('/api/pdf/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      
      const json = await res.json();
      setGenerateResult(json);
      
      if (!res.ok) {
        throw new Error(json?.error || 'Generate failed');
      }

      setSuccess('Test PDF generated successfully');
      setTimeout(() => setSuccess(null), 3000);
    } catch (e) {
      console.error('Generate error:', e);
      setError(e?.message || 'Generate failed');
    } finally {
      setBusy(false);
    }
  };

  const updatePlacementsField = (role, field, value) => {
    setPlacements((prev) => {
      const x = { ...(prev || {}) };
      x[role] = Object.assign(
        { 
          pageIndex: 0, 
          x: 380, 
          y: role === 'client' ? 120 : 60, 
          width: 160, 
          height: 60, 
          label: role === 'client' ? 'Client' : 'Attorney' 
        },
        x[role] || {}
      );
      const num = ['x', 'y', 'width', 'height', 'pageIndex', 'fontSize'].includes(field) ? Number(value) : value;
      x[role][field] = Number.isNaN(num) ? value : num;
      return x;
    });
  };

  return (
    <PageLayout>
      <Section>
        <Box sx={{ maxWidth: 1400, mx: 'auto', p: 3 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
            SmartProBono — Templates Dashboard
          </Typography>
          
          <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', mb: 4 }}>
            Manage PDF templates, signature placements, and test generation in one place.
          </Typography>

          {/* Status Messages */}
          {error && (
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}
          
          {success && (
            <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
              {success}
            </Alert>
          )}

          <Grid container spacing={3}>
            {/* Left: Templates List */}
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Templates
                  </Typography>
                  
                  <Stack spacing={2} sx={{ mb: 3 }}>
                    <Button
                      variant="outlined"
                      onClick={() => {
                        const name = prompt('Open template name?');
                        if (name) loadTemplate(name);
                      }}
                      sx={{
                        borderColor: '#1565C0',
                        color: '#1565C0',
                        '&:hover': {
                          borderColor: '#0D47A1',
                          backgroundColor: 'rgba(21, 101, 192, 0.04)',
                        },
                      }}
                    >
                      Open by Name
                    </Button>
                  </Stack>

                  <Paper variant="outlined" sx={{ maxHeight: 400, overflow: 'auto' }}>
                    <List dense>
                      {templates.map((t) => (
                        <ListItem
                          key={t.template_name}
                          button
                          selected={selected === t.template_name}
                          onClick={() => loadTemplate(t.template_name)}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'rgba(21, 101, 192, 0.08)',
                            },
                          }}
                        >
                          <ListItemText
                            primary={t.template_name}
                            secondary={
                              <Stack direction="row" spacing={1} alignItems="center">
                                <Chip 
                                  label={t.version || 'v1'} 
                                  size="small" 
                                  variant="outlined"
                                />
                                {t.base_pdf_path && (
                                  <Chip 
                                    label="Base PDF" 
                                    size="small" 
                                    color="success" 
                                    variant="outlined"
                                  />
                                )}
                              </Stack>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>
                </CardContent>
              </Card>

              {/* Base PDF Upload */}
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Base PDF
                  </Typography>
                  
                  <Stack spacing={2}>
                    <input 
                      ref={fileRef} 
                      type="file" 
                      accept="application/pdf" 
                      style={{ fontSize: '14px' }}
                    />
                    <Button
                      variant="outlined"
                      startIcon={<UploadIcon />}
                      onClick={handleUploadBasePdf}
                      disabled={busy}
                      sx={{
                        borderColor: '#1565C0',
                        color: '#1565C0',
                        '&:hover': {
                          borderColor: '#0D47A1',
                          backgroundColor: 'rgba(21, 101, 192, 0.04)',
                        },
                      }}
                    >
                      Upload / Replace
                    </Button>
                    
                    {selectedRow?.base_pdf_path && (
                      <Typography variant="caption" color="text.secondary" sx={{ wordBreak: 'break-all' }}>
                        Stored at: {selectedRow.base_pdf_path}
                      </Typography>
                    )}
                  </Stack>
                </CardContent>
              </Card>

              {/* Test Generation */}
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Test Generation
                  </Typography>
                  
                  <Button
                    variant="contained"
                    startIcon={<DownloadIcon />}
                    onClick={handleGenerateTest}
                    disabled={busy || !selected}
                    fullWidth
                    sx={{
                      backgroundColor: '#1565C0',
                      '&:hover': {
                        backgroundColor: '#0D47A1',
                      },
                    }}
                  >
                    {busy ? 'Generating...' : 'Generate Test PDF'}
                  </Button>
                  
                  {generateResult?.signedUrl && (
                    <Button
                      variant="outlined"
                      href={generateResult.signedUrl}
                      target="_blank"
                      fullWidth
                      sx={{ mt: 2 }}
                    >
                      Open Latest Test PDF
                    </Button>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Middle: Template JSON Editor */}
            <Grid item xs={12} md={5}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="h6">
                      PDFme Template JSON
                    </Typography>
                    <Button
                      variant="contained"
                      startIcon={<SaveIcon />}
                      onClick={handleSaveTemplate}
                      disabled={busy}
                      sx={{
                        backgroundColor: '#1565C0',
                        '&:hover': {
                          backgroundColor: '#0D47A1',
                        },
                      }}
                    >
                      Save Template
                    </Button>
                  </Stack>
                  
                  <TextField
                    multiline
                    fullWidth
                    rows={20}
                    value={templateJson}
                    onChange={(e) => setTemplateJson(e.target.value)}
                    placeholder="Paste designer.getTemplate() JSON here"
                    sx={{
                      '& .MuiInputBase-input': {
                        fontFamily: 'monospace',
                        fontSize: '12px',
                      },
                    }}
                  />
                </CardContent>
              </Card>
            </Grid>

            {/* Right: Signature Placements Editor */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="h6">
                      Signature Placements
                    </Typography>
                    <Button
                      variant="contained"
                      startIcon={<SaveIcon />}
                      onClick={handleSavePlacements}
                      disabled={busy || !selected}
                      sx={{
                        backgroundColor: '#1565C0',
                        '&:hover': {
                          backgroundColor: '#0D47A1',
                        },
                      }}
                    >
                      Save Placements
                    </Button>
                  </Stack>
                  
                  <Grid container spacing={2}>
                    {/* Client Placements */}
                    <Grid item xs={6}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                          Client
                        </Typography>
                        <Stack spacing={1}>
                          <TextField
                            label="X"
                            size="small"
                            type="number"
                            value={placements?.client?.x || ''}
                            onChange={(e) => updatePlacementsField('client', 'x', e.target.value)}
                          />
                          <TextField
                            label="Y"
                            size="small"
                            type="number"
                            value={placements?.client?.y || ''}
                            onChange={(e) => updatePlacementsField('client', 'y', e.target.value)}
                          />
                          <TextField
                            label="Width"
                            size="small"
                            type="number"
                            value={placements?.client?.width || ''}
                            onChange={(e) => updatePlacementsField('client', 'width', e.target.value)}
                          />
                          <TextField
                            label="Height"
                            size="small"
                            type="number"
                            value={placements?.client?.height || ''}
                            onChange={(e) => updatePlacementsField('client', 'height', e.target.value)}
                          />
                          <TextField
                            label="Page"
                            size="small"
                            type="number"
                            value={placements?.client?.pageIndex || 0}
                            onChange={(e) => updatePlacementsField('client', 'pageIndex', e.target.value)}
                          />
                          <TextField
                            label="Label"
                            size="small"
                            value={placements?.client?.label || 'Client'}
                            onChange={(e) => updatePlacementsField('client', 'label', e.target.value)}
                          />
                        </Stack>
                      </Paper>
                    </Grid>

                    {/* Attorney Placements */}
                    <Grid item xs={6}>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                          Attorney
                        </Typography>
                        <Stack spacing={1}>
                          <TextField
                            label="X"
                            size="small"
                            type="number"
                            value={placements?.attorney?.x || ''}
                            onChange={(e) => updatePlacementsField('attorney', 'x', e.target.value)}
                          />
                          <TextField
                            label="Y"
                            size="small"
                            type="number"
                            value={placements?.attorney?.y || ''}
                            onChange={(e) => updatePlacementsField('attorney', 'y', e.target.value)}
                          />
                          <TextField
                            label="Width"
                            size="small"
                            type="number"
                            value={placements?.attorney?.width || ''}
                            onChange={(e) => updatePlacementsField('attorney', 'width', e.target.value)}
                          />
                          <TextField
                            label="Height"
                            size="small"
                            type="number"
                            value={placements?.attorney?.height || ''}
                            onChange={(e) => updatePlacementsField('attorney', 'height', e.target.value)}
                          />
                          <TextField
                            label="Page"
                            size="small"
                            type="number"
                            value={placements?.attorney?.pageIndex || 0}
                            onChange={(e) => updatePlacementsField('attorney', 'pageIndex', e.target.value)}
                          />
                          <TextField
                            label="Label"
                            size="small"
                            value={placements?.attorney?.label || 'Attorney'}
                            onChange={(e) => updatePlacementsField('attorney', 'label', e.target.value)}
                          />
                        </Stack>
                      </Paper>
                    </Grid>
                  </Grid>

                  <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                    Tip: Use the visual placement page at <code>/tools/signature-placement</code> to drag boxes on a PDF preview and copy the coordinates here.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Section>
    </PageLayout>
  );
};

export default TemplatesDashboardPage;
