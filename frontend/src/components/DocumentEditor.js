import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Divider,
  Alert,
  CircularProgress,
  Tooltip,
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import UndoIcon from '@mui/icons-material/Undo';
import RedoIcon from '@mui/icons-material/Redo';
import HistoryIcon from '@mui/icons-material/History';
import PreviewIcon from '@mui/icons-material/Preview';
import { Editor } from '@tinymce/tinymce-react';
import PropTypes from 'prop-types';
const DocumentEditor = ({ documentId, initialContent, template, onSave, readOnly = false }) => {
  const [content, setContent] = useState(initialContent || '');
  const [history, setHistory] = useState([initialContent]);
  const [historyIndex, setHistoryIndex] = useState(0);
  const [showHistory, setShowHistory] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [autoSaveTimer, setAutoSaveTimer] = useState(null);
  useEffect(() => {
    return () => {
      if (autoSaveTimer) {
        clearTimeout(autoSaveTimer);
      }
    };
  }, [autoSaveTimer]);
  const handleEditorChange = newContent => {
    setContent(newContent);
    // Clear any existing auto-save timer
    if (autoSaveTimer) {
      clearTimeout(autoSaveTimer);
    }
    // Set new auto-save timer
    const timer = setTimeout(() => {
      handleSave(newContent, true);
    }, 30000); // Auto-save after 30 seconds of inactivity
    setAutoSaveTimer(timer);
  };
  const handleSave = async (contentToSave = content, isAutoSave = false) => {
    setLoading(true);
    setError(null);
    try {
      await onSave(contentToSave);
      // Add to history if not auto-save
      if (!isAutoSave) {
        setHistory(prev => [...prev.slice(0, historyIndex + 1), contentToSave]);
        setHistoryIndex(prev => prev + 1);
      }
    } catch (err) {
      setError('Failed to save document: ' + err.message);
    } finally {
      setLoading(false);
    }
  };
  const handleUndo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(prev => prev - 1);
      setContent(history[historyIndex - 1]);
    }
  };
  const handleRedo = () => {
    if (historyIndex < history.length - 1) {
      setHistoryIndex(prev => prev + 1);
      setContent(history[historyIndex + 1]);
    }
  };
  const handleRevertToVersion = index => {
    setHistoryIndex(index);
    setContent(history[index]);
    setShowHistory(false);
  };
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Toolbar */}
      <Paper sx={{ p: 1, mb: 2 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={() => handleSave()}
              disabled={loading || readOnly}
            >
              Save
            </Button>
          </Grid>
          <Grid item>
            <Tooltip title="Undo">
              <IconButton onClick={handleUndo} disabled={historyIndex === 0 || readOnly}>
                <UndoIcon />
              </IconButton>
            </Tooltip>
          </Grid>
          <Grid item>
            <Tooltip title="Redo">
              <IconButton
                onClick={handleRedo}
                disabled={historyIndex === history.length - 1 || readOnly}
              >
                <RedoIcon />
              </IconButton>
            </Tooltip>
          </Grid>
          <Grid item>
            <Tooltip title="Version History">
              <IconButton onClick={() => setShowHistory(true)}>
                <HistoryIcon />
              </IconButton>
            </Tooltip>
          </Grid>
          <Grid item>
            <Tooltip title={previewMode ? 'Edit Mode' : 'Preview Mode'}>
              <IconButton onClick={() => setPreviewMode(!previewMode)}>
                <PreviewIcon />
              </IconButton>
            </Tooltip>
          </Grid>
          {loading && (
            <Grid item>
              <CircularProgress size={24} />
            </Grid>
          )}
        </Grid>
      </Paper>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {/* Editor */}
      <Box sx={{ flexGrow: 1 }}>
        {previewMode ? (
          <Paper sx={{ p: 3, minHeight: '500px' }}>
            <div dangerouslySetInnerHTML={{ __html: content }} />
          </Paper>
        ) : (
          <Editor
            apiKey={process.env.REACT_APP_TINYMCE_API_KEY}
            value={content}
            onEditorChange={handleEditorChange}
            init={{
              height: '100%',
              menubar: true,
              plugins: [
                'advlist',
                'autolink',
                'lists',
                'link',
                'image',
                'charmap',
                'preview',
                'anchor',
                'searchreplace',
                'visualblocks',
                'code',
                'fullscreen',
                'insertdatetime',
                'media',
                'table',
                'code',
                'help',
                'wordcount',
              ],
              toolbar:
                'undo redo | blocks | ' +
                'bold italic forecolor | alignleft aligncenter ' +
                'alignright alignjustify | bullist numlist outdent indent | ' +
                'removeformat | help',
              content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
              readonly: readOnly,
            }}
          />
        )}
      </Box>
      {/* Version History Dialog */}
      <Dialog open={showHistory} onClose={() => setShowHistory(false)} maxWidth="md" fullWidth>
        <DialogTitle>Version History</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            {history.map((version, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Version {index + 1}
                  {index === historyIndex && ' (Current)'}
                </Typography>
                <Box
                  sx={{
                    p: 2,
                    bgcolor: 'grey.100',
                    borderRadius: 1,
                    maxHeight: '100px',
                    overflow: 'hidden',
                  }}
                >
                  <div dangerouslySetInnerHTML={{ __html: version.slice(0, 200) + '...' }} />
                </Box>
                <Button
                  size="small"
                  onClick={() => handleRevertToVersion(index)}
                  disabled={index === historyIndex}
                  sx={{ mt: 1 }}
                >
                  Revert to this version
                </Button>
                <Divider sx={{ mt: 2 }} />
              </Box>
            ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowHistory(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

// Define PropTypes
DocumentEditor.propTypes = {
  /** TODO: Add description */
  documentId: PropTypes.any,
  /** TODO: Add description */
  initialContent: PropTypes.any,
  /** TODO: Add description */
  template: PropTypes.any,
  /** TODO: Add description */
  onSave: PropTypes.any,
  /** TODO: Add description */
  readOnly: PropTypes.any,
};

export default DocumentEditor;