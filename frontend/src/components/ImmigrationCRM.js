import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  CircularProgress,
  Alert,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
const caseTypes = [
  'Citizenship',
  'Family-Based Immigration',
  'Employment-Based Immigration',
  'Asylum',
  'Student Visa',
  'Work Visa',
  'Green Card',
  'DACA',
  'Other',
];
const caseStatus = [
  'New',
  'In Progress',
  'Pending Documentation',
  'Under Review',
  'Approved',
  'Denied',
  'Appealing',
  'Closed',
];
const ImmigrationCRM = () => {
  const [cases, setCases] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    clientName: '',
    caseType: '',
    status: 'New',
    priority: 'Medium',
    dueDate: null,
    description: '',
    documents: [],
  });
  useEffect(() => {
    fetchCases();
  }, []);
  const fetchCases = async () => {
    setLoading(true);
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/immigration/cases');
      const data = await response.json();
      setCases(data);
    } catch (err) {
      setError('Failed to fetch cases');
    } finally {
      setLoading(false);
    }
  };
  const handleInputChange = field => event => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };
  const handleDateChange = date => {
    setFormData({
      ...formData,
      dueDate: date,
    });
  };
  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/immigration/cases', {
        method: selectedCase ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        throw new Error('Failed to save case');
      }
      fetchCases();
      handleCloseDialog();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  const handleOpenDialog = (caseData = null) => {
    if (caseData) {
      setSelectedCase(caseData);
      setFormData(caseData);
    } else {
      setSelectedCase(null);
      setFormData({
        clientName: '',
        caseType: '',
        status: 'New',
        priority: 'Medium',
        dueDate: null,
        description: '',
        documents: [],
      });
    }
    setOpenDialog(true);
  };
  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedCase(null);
    setFormData({
      clientName: '',
      caseType: '',
      status: 'New',
      priority: 'Medium',
      dueDate: null,
      description: '',
      documents: [],
    });
  };
  const handleDeleteCase = async caseId => {
    if (!window.confirm('Are you sure you want to delete this case?')) return;
    try {
      const response = await fetch(`/api/immigration/cases/${caseId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete case');
      }
      fetchCases();
    } catch (err) {
      setError(err.message);
    }
  };
  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h4">Immigration Case Management</Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={() => handleOpenDialog()}>
            New Case
          </Button>
        </Box>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Client Name</TableCell>
                <TableCell>Case Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Priority</TableCell>
                <TableCell>Due Date</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : (
                cases.map(caseItem => (
                  <TableRow key={caseItem.id}>
                    <TableCell>{caseItem.clientName}</TableCell>
                    <TableCell>{caseItem.caseType}</TableCell>
                    <TableCell>
                      <Chip
                        label={caseItem.status}
                        color={
                          caseItem.status === 'Approved'
                            ? 'success'
                            : caseItem.status === 'Denied'
                              ? 'error'
                              : caseItem.status === 'In Progress'
                                ? 'primary'
                                : 'default'
                        }
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={caseItem.priority}
                        color={
                          caseItem.priority === 'High'
                            ? 'error'
                            : caseItem.priority === 'Medium'
                              ? 'warning'
                              : 'info'
                        }
                      />
                    </TableCell>
                    <TableCell>{new Date(caseItem.dueDate).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <IconButton onClick={() => handleOpenDialog(caseItem)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton onClick={() => handleDeleteCase(caseItem.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
          <DialogTitle>{selectedCase ? 'Edit Case' : 'New Case'}</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Client Name"
                  value={formData.clientName}
                  onChange={handleInputChange('clientName')}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth required>
                  <InputLabel>Case Type</InputLabel>
                  <Select
                    value={formData.caseType}
                    onChange={handleInputChange('caseType')}
                    label="Case Type"
                  >
                    {caseTypes.map(type => (
                      <MenuItem key={type} value={type}>
                        {type}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    value={formData.status}
                    onChange={handleInputChange('status')}
                    label="Status"
                  >
                    {caseStatus.map(status => (
                      <MenuItem key={status} value={status}>
                        {status}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Priority</InputLabel>
                  <Select
                    value={formData.priority}
                    onChange={handleInputChange('priority')}
                    label="Priority"
                  >
                    <MenuItem value="High">High</MenuItem>
                    <MenuItem value="Medium">Medium</MenuItem>
                    <MenuItem value="Low">Low</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <DatePicker
                  label="Due Date"
                  value={formData.dueDate}
                  onChange={handleDateChange}
                  renderInput={params => <TextField {...params} fullWidth />}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Description"
                  value={formData.description}
                  onChange={handleInputChange('description')}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button onClick={handleSubmit} variant="contained" disabled={loading}>
              {loading ? <CircularProgress size={24} /> : 'Save'}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};
export default ImmigrationCRM;