import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Tabs,
  Tab,
  Badge,
  Paper,
  Divider,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Person as PersonIcon,
  Case as CaseIcon,
  CalendarToday as CalendarIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Assignment as AssignmentIcon,
  Timeline as TimelineIcon,
  AttachMoney as MoneyIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';
import CRMService from '../services/CRMService';

const VirtualParalegalCRM = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [clients, setClients] = useState([]);
  const [cases, setCases] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);

  // Test CRM connection
  const testCRMConnection = async () => {
    try {
      setLoading(true);
      const healthCheck = await CRMService.healthCheck();
      console.log('✅ CRM Service connected:', healthCheck);
      setError(null);
    } catch (error) {
      console.error('❌ CRM Service connection failed:', error);
      setError('CRM Service not available. Using demo data.');
    } finally {
      setLoading(false);
    }
  };

  // Load data and test CRM connection
  useEffect(() => {
    testCRMConnection();
    setClients([
      {
        id: 1,
        name: 'John Smith',
        email: 'john.smith@email.com',
        phone: '(555) 123-4567',
        status: 'active',
        cases: 3,
        lastContact: '2025-09-08',
        avatar: 'JS'
      },
      {
        id: 2,
        name: 'Maria Garcia',
        email: 'maria.garcia@email.com',
        phone: '(555) 234-5678',
        status: 'active',
        cases: 1,
        lastContact: '2025-09-07',
        avatar: 'MG'
      },
      {
        id: 3,
        name: 'Robert Johnson',
        email: 'robert.j@email.com',
        phone: '(555) 345-6789',
        status: 'inactive',
        cases: 0,
        lastContact: '2025-08-15',
        avatar: 'RJ'
      }
    ]);

    setCases([
      {
        id: 1,
        clientId: 1,
        title: 'Immigration - Green Card Application',
        type: 'Immigration',
        status: 'in_progress',
        priority: 'high',
        dueDate: '2025-10-15',
        progress: 65,
        documents: 12,
        lastUpdate: '2025-09-09'
      },
      {
        id: 2,
        clientId: 1,
        title: 'Divorce Proceedings',
        type: 'Family Law',
        status: 'pending',
        priority: 'medium',
        dueDate: '2025-11-20',
        progress: 30,
        documents: 8,
        lastUpdate: '2025-09-05'
      },
      {
        id: 3,
        clientId: 2,
        title: 'Employment Contract Review',
        type: 'Employment',
        status: 'completed',
        priority: 'low',
        dueDate: '2025-09-01',
        progress: 100,
        documents: 5,
        lastUpdate: '2025-09-01'
      }
    ]);

    setTasks([
      {
        id: 1,
        caseId: 1,
        title: 'File I-485 Application',
        type: 'document',
        status: 'pending',
        dueDate: '2025-09-15',
        priority: 'high'
      },
      {
        id: 2,
        caseId: 1,
        title: 'Schedule Biometrics Appointment',
        type: 'appointment',
        status: 'in_progress',
        dueDate: '2025-09-12',
        priority: 'medium'
      },
      {
        id: 3,
        caseId: 2,
        title: 'Gather Financial Documents',
        type: 'research',
        status: 'completed',
        dueDate: '2025-09-08',
        priority: 'low'
      }
    ]);
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleOpenDialog = (type, item = null) => {
    setDialogType(type);
    setSelectedItem(item);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedItem(null);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
      case 'completed':
      case 'in_progress':
        return 'success';
      case 'pending':
        return 'warning';
      case 'inactive':
      case 'overdue':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const renderClientsTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Clients ({clients.length})</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog('client')}
        >
          Add Client
        </Button>
      </Box>

      <Grid container spacing={3}>
        {clients.map((client) => (
          <Grid item xs={12} md={6} lg={4} key={client.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                    {client.avatar}
                  </Avatar>
                  <Box>
                    <Typography variant="h6">{client.name}</Typography>
                    <Chip
                      label={client.status}
                      color={getStatusColor(client.status)}
                      size="small"
                    />
                  </Box>
                </Box>
                
                <List dense>
                  <ListItem>
                    <ListItemAvatar>
                      <EmailIcon fontSize="small" />
                    </ListItemAvatar>
                    <ListItemText primary={client.email} />
                  </ListItem>
                  <ListItem>
                    <ListItemAvatar>
                      <PhoneIcon fontSize="small" />
                    </ListItemAvatar>
                    <ListItemText primary={client.phone} />
                  </ListItem>
                  <ListItem>
                    <ListItemAvatar>
                      <CaseIcon fontSize="small" />
                    </ListItemAvatar>
                    <ListItemText primary={`${client.cases} active cases`} />
                  </ListItem>
                </List>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => handleOpenDialog('client', client)}>
                  <EditIcon />
                </Button>
                <Button size="small" color="error">
                  <DeleteIcon />
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderCasesTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Cases ({cases.length})</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog('case')}
        >
          Add Case
        </Button>
      </Box>

      <Grid container spacing={3}>
        {cases.map((caseItem) => (
          <Grid item xs={12} md={6} lg={4} key={caseItem.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    {caseItem.title}
                  </Typography>
                  <Chip
                    label={caseItem.priority}
                    color={getPriorityColor(caseItem.priority)}
                    size="small"
                  />
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {caseItem.type}
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">Progress</Typography>
                    <Typography variant="body2">{caseItem.progress}%</Typography>
                  </Box>
                  <Box sx={{ width: '100%', bgcolor: 'grey.200', borderRadius: 1 }}>
                    <Box
                      sx={{
                        width: `${caseItem.progress}%`,
                        height: 8,
                        bgcolor: 'primary.main',
                        borderRadius: 1
                      }}
                    />
                  </Box>
                </Box>

                <List dense>
                  <ListItem>
                    <ListItemAvatar>
                      <CalendarIcon fontSize="small" />
                    </ListItemAvatar>
                    <ListItemText primary={`Due: ${caseItem.dueDate}`} />
                  </ListItem>
                  <ListItem>
                    <ListItemAvatar>
                      <AssignmentIcon fontSize="small" />
                    </ListItemAvatar>
                    <ListItemText primary={`${caseItem.documents} documents`} />
                  </ListItem>
                </List>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => handleOpenDialog('case', caseItem)}>
                  <EditIcon />
                </Button>
                <Button size="small" color="error">
                  <DeleteIcon />
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderTasksTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Tasks ({tasks.length})</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog('task')}
        >
          Add Task
        </Button>
      </Box>

      <List>
        {tasks.map((task) => (
          <ListItem key={task.id} divider>
            <ListItemAvatar>
              <Avatar sx={{ bgcolor: getStatusColor(task.status) === 'success' ? 'success.main' : 'primary.main' }}>
                {task.status === 'completed' ? <CheckIcon /> : <AssignmentIcon />}
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={task.title}
              secondary={`Due: ${task.dueDate} • ${task.type}`}
            />
            <ListItemSecondaryAction>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Chip
                  label={task.priority}
                  color={getPriorityColor(task.priority)}
                  size="small"
                />
                <IconButton size="small" onClick={() => handleOpenDialog('task', task)}>
                  <EditIcon />
                </IconButton>
              </Box>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderDialog = () => (
    <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
      <DialogTitle>
        {dialogType === 'client' ? 'Add/Edit Client' :
         dialogType === 'case' ? 'Add/Edit Case' :
         'Add/Edit Task'}
      </DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Name"
          fullWidth
          variant="outlined"
          defaultValue={selectedItem?.name || selectedItem?.title || ''}
        />
        {dialogType === 'client' && (
          <>
            <TextField
              margin="dense"
              label="Email"
              type="email"
              fullWidth
              variant="outlined"
              defaultValue={selectedItem?.email || ''}
            />
            <TextField
              margin="dense"
              label="Phone"
              fullWidth
              variant="outlined"
              defaultValue={selectedItem?.phone || ''}
            />
          </>
        )}
        {dialogType === 'case' && (
          <>
            <TextField
              margin="dense"
              label="Type"
              fullWidth
              variant="outlined"
              defaultValue={selectedItem?.type || ''}
            />
            <TextField
              margin="dense"
              label="Due Date"
              type="date"
              fullWidth
              variant="outlined"
              InputLabelProps={{ shrink: true }}
              defaultValue={selectedItem?.dueDate || ''}
            />
          </>
        )}
        {dialogType === 'task' && (
          <>
            <TextField
              margin="dense"
              label="Type"
              fullWidth
              variant="outlined"
              defaultValue={selectedItem?.type || ''}
            />
            <TextField
              margin="dense"
              label="Due Date"
              type="date"
              fullWidth
              variant="outlined"
              InputLabelProps={{ shrink: true }}
              defaultValue={selectedItem?.dueDate || ''}
            />
          </>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCloseDialog}>Cancel</Button>
        <Button variant="contained" onClick={handleCloseDialog}>
          {selectedItem ? 'Update' : 'Create'}
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Virtual Paralegal CRM
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage your clients, cases, and tasks efficiently
        </Typography>
        
        {/* Connection Status */}
        {loading && (
          <Alert severity="info" sx={{ mt: 2 }}>
            <CircularProgress size={20} sx={{ mr: 1 }} />
            Testing CRM connection...
          </Alert>
        )}
        
        {error && (
          <Alert severity="warning" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        
        {!loading && !error && (
          <Alert severity="success" sx={{ mt: 2 }}>
            ✅ CRM Service Connected
          </Alert>
        )}
      </Box>

      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label="Clients" />
          <Tab label="Cases" />
          <Tab label="Tasks" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {activeTab === 0 && renderClientsTab()}
          {activeTab === 1 && renderCasesTab()}
          {activeTab === 2 && renderTasksTab()}
        </Box>
      </Paper>

      {renderDialog()}
    </Container>
  );
};

export default VirtualParalegalCRM;
