import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Button,
  TextField,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Avatar,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  LinearProgress,
  Paper,
  Divider
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Person as PersonIcon,
  Description as DescriptionIcon,
  Event as EventIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
  Business as BusinessIcon,
  Assignment as AssignmentIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  LowPriority as PriorityIcon,
  Category as CategoryIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const VirtualParalegalPage = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [clients, setClients] = useState([]);
  const [cases, setCases] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);
  const [loading, setLoading] = useState(false);

  // Sample data - in real app, this would come from API
  useEffect(() => {
    setClients([
      {
        id: 1,
        name: 'John Smith',
        email: 'john.smith@email.com',
        phone: '(555) 123-4567',
        address: '123 Main St, Providence, RI',
        caseType: 'Immigration',
        status: 'Active',
        lastContact: '2024-01-15'
      },
      {
        id: 2,
        name: 'Maria Garcia',
        email: 'maria.garcia@email.com',
        phone: '(555) 987-6543',
        address: '456 Oak Ave, Providence, RI',
        caseType: 'Family Law',
        status: 'Pending',
        lastContact: '2024-01-10'
      }
    ]);

    setCases([
      {
        id: 1,
        clientId: 1,
        title: 'Green Card Application',
        type: 'Immigration',
        status: 'In Progress',
        priority: 'High',
        dueDate: '2024-02-15',
        progress: 65
      },
      {
        id: 2,
        clientId: 2,
        title: 'Divorce Proceedings',
        type: 'Family Law',
        status: 'Review',
        priority: 'Medium',
        dueDate: '2024-02-28',
        progress: 30
      }
    ]);

    setTasks([
      {
        id: 1,
        title: 'Review immigration documents',
        caseId: 1,
        dueDate: '2024-01-20',
        status: 'Pending',
        priority: 'High'
      },
      {
        id: 2,
        title: 'Schedule client meeting',
        caseId: 2,
        dueDate: '2024-01-18',
        status: 'Completed',
        priority: 'Medium'
      }
    ]);

    setDocuments([
      {
        id: 1,
        name: 'I-485 Application',
        type: 'Form',
        caseId: 1,
        status: 'Draft',
        lastModified: '2024-01-15'
      },
      {
        id: 2,
        name: 'Divorce Petition',
        type: 'Legal Document',
        caseId: 2,
        status: 'Review',
        lastModified: '2024-01-12'
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
      case 'Active':
      case 'Completed':
      case 'In Progress':
        return 'success';
      case 'Pending':
      case 'Review':
        return 'warning';
      case 'Overdue':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High':
        return 'error';
      case 'Medium':
        return 'warning';
      case 'Low':
        return 'success';
      default:
        return 'default';
    }
  };

  const renderClientsTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Client Management</Typography>
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
                    <PersonIcon />
                  </Avatar>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h6">{client.name}</Typography>
                    <Chip
                      label={client.status}
                      size="small"
                      color={getStatusColor(client.status)}
                    />
                  </Box>
                  <IconButton onClick={() => handleOpenDialog('client', client)}>
                    <EditIcon />
                  </IconButton>
                </Box>

                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <EmailIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={client.email} />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <PhoneIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={client.phone} />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <LocationIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={client.address} />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <BusinessIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={client.caseType} />
                  </ListItem>
                </List>

                <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid #eee' }}>
                  <Typography variant="caption" color="text.secondary">
                    Last Contact: {client.lastContact}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderCasesTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Case Management</Typography>
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
          <Grid item xs={12} md={6} key={caseItem.id}>
            <Card>
              <CardHeader
                title={caseItem.title}
                subheader={`Client: ${clients.find(c => c.id === caseItem.clientId)?.name || 'Unknown'}`}
                action={
                  <Box>
                    <Chip
                      label={caseItem.status}
                      size="small"
                      color={getStatusColor(caseItem.status)}
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={caseItem.priority}
                      size="small"
                      color={getPriorityColor(caseItem.priority)}
                    />
                  </Box>
                }
              />
              <CardContent>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Progress
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={caseItem.progress}
                    sx={{ mb: 1 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    {caseItem.progress}% Complete
                  </Typography>
                </Box>

                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <CategoryIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={caseItem.type} />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <EventIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={`Due: ${caseItem.dueDate}`} />
                  </ListItem>
                </List>

                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                  <Button
                    size="small"
                    startIcon={<EditIcon />}
                    onClick={() => handleOpenDialog('case', caseItem)}
                  >
                    Edit
                  </Button>
                  <Button
                    size="small"
                    startIcon={<DescriptionIcon />}
                    onClick={() => handleOpenDialog('documents', caseItem)}
                  >
                    Documents
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderTasksTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Task Management</Typography>
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
            <ListItemIcon>
              <AssignmentIcon />
            </ListItemIcon>
            <ListItemText
              primary={task.title}
              secondary={`Case: ${cases.find(c => c.id === task.caseId)?.title || 'Unknown'} • Due: ${task.dueDate}`}
            />
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip
                label={task.priority}
                size="small"
                color={getPriorityColor(task.priority)}
              />
              <Chip
                label={task.status}
                size="small"
                color={getStatusColor(task.status)}
              />
              <IconButton onClick={() => handleOpenDialog('task', task)}>
                <EditIcon />
              </IconButton>
            </Box>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderDocumentsTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Document Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog('document')}
        >
          Add Document
        </Button>
      </Box>

      <List>
        {documents.map((doc) => (
          <ListItem key={doc.id} divider>
            <ListItemIcon>
              <DescriptionIcon />
            </ListItemIcon>
            <ListItemText
              primary={doc.name}
              secondary={`Case: ${cases.find(c => c.id === doc.caseId)?.title || 'Unknown'} • Modified: ${doc.lastModified}`}
            />
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip
                label={doc.type}
                size="small"
                variant="outlined"
              />
              <Chip
                label={doc.status}
                size="small"
                color={getStatusColor(doc.status)}
              />
              <IconButton onClick={() => handleOpenDialog('document', doc)}>
                <EditIcon />
              </IconButton>
            </Box>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderDialog = () => (
    <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
      <DialogTitle>
        {selectedItem ? 'Edit' : 'Add'} {dialogType.charAt(0).toUpperCase() + dialogType.slice(1)}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 2 }}>
          <TextField
            fullWidth
            label="Name"
            margin="normal"
            defaultValue={selectedItem?.name || ''}
          />
          {dialogType === 'client' && (
            <>
              <TextField
                fullWidth
                label="Email"
                type="email"
                margin="normal"
                defaultValue={selectedItem?.email || ''}
              />
              <TextField
                fullWidth
                label="Phone"
                margin="normal"
                defaultValue={selectedItem?.phone || ''}
              />
              <TextField
                fullWidth
                label="Address"
                margin="normal"
                defaultValue={selectedItem?.address || ''}
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Case Type</InputLabel>
                <Select defaultValue={selectedItem?.caseType || ''}>
                  <MenuItem value="Immigration">Immigration</MenuItem>
                  <MenuItem value="Family Law">Family Law</MenuItem>
                  <MenuItem value="Criminal Law">Criminal Law</MenuItem>
                  <MenuItem value="Business Law">Business Law</MenuItem>
                </Select>
              </FormControl>
            </>
          )}
          {dialogType === 'case' && (
            <>
              <FormControl fullWidth margin="normal">
                <InputLabel>Client</InputLabel>
                <Select defaultValue={selectedItem?.clientId || ''}>
                  {clients.map((client) => (
                    <MenuItem key={client.id} value={client.id}>
                      {client.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl fullWidth margin="normal">
                <InputLabel>Priority</InputLabel>
                <Select defaultValue={selectedItem?.priority || ''}>
                  <MenuItem value="High">High</MenuItem>
                  <MenuItem value="Medium">Medium</MenuItem>
                  <MenuItem value="Low">Low</MenuItem>
                </Select>
              </FormControl>
            </>
          )}
        </Box>
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
    <PageLayout
      title="Virtual Paralegal"
      description="Manage clients, cases, tasks, and documents efficiently"
    >
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Virtual Paralegal Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Streamline your legal practice with our comprehensive case management system
          </Typography>
        </Box>

        <Paper sx={{ mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} variant="fullWidth">
            <Tab label="Clients" icon={<PersonIcon />} />
            <Tab label="Cases" icon={<AssignmentIcon />} />
            <Tab label="Tasks" icon={<CheckCircleIcon />} />
            <Tab label="Documents" icon={<DescriptionIcon />} />
          </Tabs>
        </Paper>

        <Box sx={{ mt: 3 }}>
          {activeTab === 0 && renderClientsTab()}
          {activeTab === 1 && renderCasesTab()}
          {activeTab === 2 && renderTasksTab()}
          {activeTab === 3 && renderDocumentsTab()}
        </Box>

        {renderDialog()}
      </Container>
    </PageLayout>
  );
};

export default VirtualParalegalPage;