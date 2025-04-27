import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Grid,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Comment as CommentIcon,
  Attachment as AttachmentIcon,
} from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';

interface FormSubmission {
  _id: string;
  template_id: string;
  status: string;
  created_at: string;
  updated_at: string;
  data: any;
  comments: Comment[];
  attachments: Attachment[];
}

interface Comment {
  _id: string;
  content: string;
  user_id: string;
  created_at: string;
}

interface Attachment {
  _id: string;
  filename: string;
  url: string;
}

const FormManager: React.FC = () => {
  const [forms, setForms] = useState<FormSubmission[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedForm, setSelectedForm] = useState<FormSubmission | null>(null);
  const [commentDialogOpen, setCommentDialogOpen] = useState(false);
  const [newComment, setNewComment] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetchForms();
  }, [page, rowsPerPage]);

  const fetchForms = async () => {
    try {
      const response = await api.get('/api/immigration/forms/search', {
        params: {
          page: page + 1,
          per_page: rowsPerPage,
        },
      });
      setForms(response.data.forms);
      setLoading(false);
    } catch (err) {
      setError('Failed to load forms');
      setLoading(false);
    }
  };

  const handleStatusChange = async (formId: string, newStatus: string) => {
    try {
      await api.put(`/api/immigration/forms/${formId}/status`, {
        status: newStatus,
      });
      fetchForms();
    } catch (err) {
      setError('Failed to update form status');
    }
  };

  const handleCommentSubmit = async () => {
    if (!selectedForm || !newComment.trim()) return;

    try {
      await api.post(`/api/immigration/forms/${selectedForm._id}/comments`, {
        content: newComment,
      });
      setNewComment('');
      setCommentDialogOpen(false);
      fetchForms();
    } catch (err) {
      setError('Failed to add comment');
    }
  };

  const handleAttachmentUpload = async (formId: string, file: File) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      await api.post(`/api/immigration/forms/${formId}/attachments`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      fetchForms();
    } catch (err) {
      setError('Failed to upload attachment');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Form ID</TableCell>
                <TableCell>Template</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Updated</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {forms.map((form) => (
                <TableRow key={form._id}>
                  <TableCell>{form._id}</TableCell>
                  <TableCell>{form.template_id}</TableCell>
                  <TableCell>
                    <Chip
                      label={form.status}
                      color={
                        form.status === 'approved'
                          ? 'success'
                          : form.status === 'rejected'
                          ? 'error'
                          : 'default'
                      }
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(form.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    {new Date(form.updated_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      onClick={() => {
                        setSelectedForm(form);
                        setCommentDialogOpen(true);
                      }}
                    >
                      <CommentIcon />
                    </IconButton>
                    <IconButton component="label">
                      <AttachmentIcon />
                      <input
                        type="file"
                        hidden
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) {
                            handleAttachmentUpload(form._id, file);
                          }
                        }}
                      />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={forms.length}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
        />
      </Paper>

      <Dialog
        open={commentDialogOpen}
        onClose={() => setCommentDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add Comment</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Comment"
            fullWidth
            multiline
            rows={4}
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
          />
          {selectedForm?.comments && (
            <Box mt={2}>
              <Typography variant="h6">Previous Comments</Typography>
              {selectedForm.comments.map((comment) => (
                <Card key={comment._id} sx={{ mt: 1 }}>
                  <CardContent>
                    <Typography variant="body2" color="textSecondary">
                      {new Date(comment.created_at).toLocaleString()}
                    </Typography>
                    <Typography>{comment.content}</Typography>
                  </CardContent>
                </Card>
              ))}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCommentDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCommentSubmit} variant="contained" color="primary">
            Add Comment
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default FormManager; 