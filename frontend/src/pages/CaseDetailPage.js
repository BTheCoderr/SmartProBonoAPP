import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Divider,
  Chip,
  Button,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Stepper,
  Step,
  StepLabel,
  IconButton,
  Card,
  CardContent,
  CardActions,
  CircularProgress,
  Tab,
  Tabs,
  Menu,
  MenuItem,
  Tooltip,
  Alert,
} from '@mui/material';
// Icons
import PersonIcon from '@mui/icons-material/Person';
import AssignmentIcon from '@mui/icons-material/Assignment';
import EventIcon from '@mui/icons-material/Event';
import ScheduleIcon from '@mui/icons-material/Schedule';
import DescriptionIcon from '@mui/icons-material/Description';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import MoreTimeIcon from '@mui/icons-material/MoreTime';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import CallIcon from '@mui/icons-material/Call';
import EmailIcon from '@mui/icons-material/Email';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import DownloadIcon from '@mui/icons-material/Download';
import ShareIcon from '@mui/icons-material/Share';
import DeleteIcon from '@mui/icons-material/Delete';
import ArchiveIcon from '@mui/icons-material/Archive';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import LocalPrintshopIcon from '@mui/icons-material/LocalPrintshop';
import ShieldIcon from '@mui/icons-material/Shield';
// Components
import Navigation from '../components/Navigation';
import { format } from 'date-fns';
// Data
import {
  getCaseById as getCase,
  getStatusLabel,
  getCaseTypeLabel,
  getPriorityLabel,
  CASE_STATUS,
} from '../data/casesData';
import { getCaseById } from '../services/caseService';
const CaseDetailPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { caseId } = useParams();
  // State
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [menuAnchorEl, setMenuAnchorEl] = useState(null);
  // Menu state
  const menuOpen = Boolean(menuAnchorEl);
  // Fetch case data
  useEffect(() => {
    const fetchCaseData = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getCaseById(caseId);
        if (data) {
          setCaseData(data);
        } else {
          setError('Case not found');
        }
      } catch (err) {
        console.error('Error loading case data:', err);
        setError('Error loading case data');
      } finally {
        setLoading(false);
      }
    };
    fetchCaseData();
  }, [caseId]);
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  // Menu handlers
  const handleMenuOpen = event => {
    setMenuAnchorEl(event.currentTarget);
  };
  const handleMenuClose = () => {
    setMenuAnchorEl(null);
  };
  // Action handlers
  const handleEdit = () => {
    navigate(`/cases/${caseId}/edit`);
    handleMenuClose();
  };
  const handleAddUpdate = () => {
    // Logic to add update to timeline
    handleMenuClose();
  };
  const handleAddDocument = () => {
    // Logic to add document
    handleMenuClose();
  };
  const handleStatusChange = newStatus => {
    // Logic to change case status
    handleMenuClose();
  };
  const handleMarkComplete = () => {
    handleStatusChange(CASE_STATUS.RESOLVED);
  };
  const handleArchiveCase = () => {
    // Logic to archive case
    handleMenuClose();
  };
  // Handle safety monitor navigation
  const handleSafetyMonitor = () => {
    navigate(`/cases/${caseId}/safety`);
    handleMenuClose();
  };
  // Get progress step based on status
  const getProgressStep = status => {
    const statusOrder = {
      [CASE_STATUS.NEW]: 0,
      [CASE_STATUS.IN_PROGRESS]: 1,
      [CASE_STATUS.PENDING_CLIENT]: 2,
      [CASE_STATUS.PENDING_COURT]: 2,
      [CASE_STATUS.RESOLVED]: 3,
      [CASE_STATUS.CLOSED]: 4,
    };
    return statusOrder[status] || 0;
  };
  // Go back to cases list
  const handleBackToList = () => {
    navigate('/cases');
  };
  // Show loading spinner while data is loading
  if (loading) {
    return (
      <Box>
        <Navigation />
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              {t('Loading case details...')}
            </Typography>
          </Box>
        </Container>
      </Box>
    );
  }
  // Show error message
  if (error) {
    return (
      <Box>
        <Navigation />
        <Container maxWidth="lg">
          <Box sx={{ mt: 4, mb: 2 }}>
            <Button
              variant="outlined"
              startIcon={<ArrowBackIcon />}
              onClick={handleBackToList}
              size="small"
            >
              {t('Back to Cases')}
            </Button>
          </Box>
          <Alert severity="error" sx={{ my: 4 }}>
            <Typography variant="subtitle1" gutterBottom>
              {t(error)}
            </Typography>
            <Typography variant="body2">
              {t(
                'The requested case could not be found or accessed. Please check the URL or go back to the cases list.'
              )}
            </Typography>
          </Alert>
          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/cases/new')}
              sx={{ mr: 2 }}
            >
              {t('Create New Case')}
            </Button>
            <Button variant="outlined" onClick={handleBackToList}>
              {t('View All Cases')}
            </Button>
          </Box>
        </Container>
      </Box>
    );
  }
  return (
    <Box>
      <Navigation />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
        {/* Header with back button and actions */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Button variant="outlined" startIcon={<ArrowBackIcon />} onClick={handleBackToList}>
            {t('Back to Cases')}
          </Button>
          <Box>
            <Button
              variant="contained"
              startIcon={<EditIcon />}
              onClick={handleEdit}
              sx={{ mr: 1 }}
            >
              {t('Edit Case')}
            </Button>
            <Button variant="outlined" endIcon={<MoreVertIcon />} onClick={handleMenuOpen}>
              {t('Actions')}
            </Button>
            <Menu anchorEl={menuAnchorEl} open={menuOpen} onClose={handleMenuClose}>
              <MenuItem onClick={handleAddUpdate}>
                <ListItemIcon>
                  <AddIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>{t('Add Update')}</ListItemText>
              </MenuItem>
              <MenuItem onClick={handleAddDocument}>
                <ListItemIcon>
                  <AttachFileIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>{t('Add Document')}</ListItemText>
              </MenuItem>
              <MenuItem onClick={handleSafetyMonitor}>
                <ListItemIcon>
                  <ShieldIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>{t('Safety Monitor')}</ListItemText>
              </MenuItem>
              <Divider />
              <MenuItem onClick={handleMarkComplete}>
                <ListItemIcon>
                  <CheckCircleIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>{t('Mark as Complete')}</ListItemText>
              </MenuItem>
              <MenuItem onClick={handleArchiveCase}>
                <ListItemIcon>
                  <ArchiveIcon fontSize="small" />
                </ListItemIcon>
                <ListItemText>{t('Archive Case')}</ListItemText>
              </MenuItem>
            </Menu>
          </Box>
        </Box>
        {/* Case header */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap' }}>
            <Box sx={{ maxWidth: '80%' }}>
              <Typography variant="h4" component="h1" gutterBottom>
                {caseData.title}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                <Chip
                  label={getStatusLabel(caseData.status)}
                  color={
                    caseData.status === CASE_STATUS.RESOLVED ||
                    caseData.status === CASE_STATUS.CLOSED
                      ? 'success'
                      : caseData.status === CASE_STATUS.IN_PROGRESS
                        ? 'primary'
                        : caseData.status === CASE_STATUS.PENDING_CLIENT ||
                            caseData.status === CASE_STATUS.PENDING_COURT
                          ? 'warning'
                          : 'default'
                  }
                />
                <Chip label={getCaseTypeLabel(caseData.type)} />
                <Chip
                  label={getPriorityLabel(caseData.priority)}
                  color={
                    caseData.priority === 'urgent'
                      ? 'error'
                      : caseData.priority === 'high'
                        ? 'warning'
                        : caseData.priority === 'medium'
                          ? 'info'
                          : 'default'
                  }
                />
                <Chip icon={<AssignmentIcon />} label={`Case #${caseData.id}`} variant="outlined" />
              </Box>
              <Typography variant="body1">{caseData.description}</Typography>
            </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                <EventIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                {t('Created')}: {format(new Date(caseData.created), 'MMM d, yyyy')}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <ScheduleIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                {t('Last Updated')}: {format(new Date(caseData.updated), 'MMM d, yyyy')}
              </Typography>
            </Box>
          </Box>
          {/* Progress stepper */}
          <Box sx={{ mt: 4 }}>
            <Stepper activeStep={getProgressStep(caseData.status)}>
              <Step key="new">
                <StepLabel>{t('New')}</StepLabel>
              </Step>
              <Step key="in_progress">
                <StepLabel>{t('In Progress')}</StepLabel>
              </Step>
              <Step key="pending">
                <StepLabel>{t('Pending Action')}</StepLabel>
              </Step>
              <Step key="resolved">
                <StepLabel>{t('Resolved')}</StepLabel>
              </Step>
              <Step key="closed">
                <StepLabel>{t('Closed')}</StepLabel>
              </Step>
            </Stepper>
          </Box>
        </Paper>
        {/* Tab navigation */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 4 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="case detail tabs">
            <Tab label={t('Details')} id="tab-0" />
            <Tab label={t('Timeline')} id="tab-1" />
            <Tab label={t('Documents')} id="tab-2" />
            <Tab label={t('Next Steps')} id="tab-3" />
            <Tab label={t('Safety Monitor')} id="tab-4" />
          </Tabs>
        </Box>
        {/* Details tab */}
        {tabValue === 0 && (
          <Grid container spacing={4}>
            {/* Client information */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <PersonIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                  {t('Client Information')}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
                  <Avatar sx={{ mr: 2 }}>{caseData.client.name.charAt(0)}</Avatar>
                  <Box>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                      {caseData.client.name}
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}
                      >
                        <CallIcon fontSize="small" sx={{ mr: 1 }} />
                        {caseData.client.phone}
                      </Typography>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}
                      >
                        <EmailIcon fontSize="small" sx={{ mr: 1 }} />
                        {caseData.client.email}
                      </Typography>
                    </Box>
                    <Box sx={{ mt: 1 }}>
                      <Button
                        size="small"
                        startIcon={<CallIcon />}
                        variant="outlined"
                        sx={{ mr: 1 }}
                      >
                        {t('Call')}
                      </Button>
                      <Button size="small" startIcon={<EmailIcon />} variant="outlined">
                        {t('Email')}
                      </Button>
                    </Box>
                  </Box>
                </Box>
              </Paper>
            </Grid>
            {/* Attorney information */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <AssignmentTurnedInIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                  {t('Attorney Information')}
                </Typography>
                <Divider sx={{ mb: 2 }} />
                {caseData.assignedTo ? (
                  <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
                    <Avatar sx={{ mr: 2 }}>{caseData.assignedTo.name.charAt(0)}</Avatar>
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                        {caseData.assignedTo.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {caseData.assignedTo.role}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}
                        >
                          <CallIcon fontSize="small" sx={{ mr: 1 }} />
                          {caseData.assignedTo.phone}
                        </Typography>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}
                        >
                          <EmailIcon fontSize="small" sx={{ mr: 1 }} />
                          {caseData.assignedTo.email}
                        </Typography>
                      </Box>
                      <Box sx={{ mt: 1 }}>
                        <Button
                          size="small"
                          startIcon={<CallIcon />}
                          variant="outlined"
                          sx={{ mr: 1 }}
                        >
                          {t('Call')}
                        </Button>
                        <Button size="small" startIcon={<EmailIcon />} variant="outlined">
                          {t('Email')}
                        </Button>
                      </Box>
                    </Box>
                  </Box>
                ) : (
                  <Box sx={{ textAlign: 'center', py: 2 }}>
                    <Typography variant="body1" color="text.secondary">
                      {t('No attorney assigned')}
                    </Typography>
                    <Button variant="outlined" startIcon={<PersonIcon />} sx={{ mt: 1 }}>
                      {t('Assign Attorney')}
                    </Button>
                  </Box>
                )}
              </Paper>
            </Grid>
          </Grid>
        )}
        {/* Timeline tab */}
        {tabValue === 1 && (
          <Paper sx={{ p: 3 }}>
            <Box
              sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}
            >
              <Typography variant="h6">{t('Case Timeline')}</Typography>
              <Button variant="outlined" startIcon={<AddIcon />} onClick={handleAddUpdate}>
                {t('Add Update')}
              </Button>
            </Box>
            <List>
              {caseData.timeline.map((event, index) => (
                <React.Fragment key={`timeline-${index}`}>
                  <ListItem
                    alignItems="flex-start"
                    sx={{
                      position: 'relative',
                      pl: 4,
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        left: '20px',
                        top: 0,
                        bottom: 0,
                        width: '2px',
                        bgcolor: 'divider',
                        display: index === caseData.timeline.length - 1 ? 'none' : 'block',
                      },
                    }}
                  >
                    <ListItemIcon
                      sx={{
                        position: 'absolute',
                        left: '12px',
                        top: '16px',
                        height: '16px',
                        width: '16px',
                        minWidth: 'auto',
                      }}
                    >
                      <Box
                        sx={{
                          height: '16px',
                          width: '16px',
                          borderRadius: '50%',
                          bgcolor: 'primary.main',
                          border: '3px solid white',
                        }}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="subtitle1">{event.title}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {format(new Date(event.date), 'MMM d, yyyy h:mm a')}
                          </Typography>
                        </Box>
                      }
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          <Typography variant="body2" paragraph>
                            {event.description}
                          </Typography>
                          {event.actor && (
                            <Typography variant="caption" color="text.secondary">
                              {t('By')}: {event.actor}
                            </Typography>
                          )}
                        </Box>
                      }
                    />
                  </ListItem>
                </React.Fragment>
              ))}
            </List>
          </Paper>
        )}
        {/* Documents tab */}
        {tabValue === 2 && (
          <Box>
            <Box
              sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}
            >
              <Typography variant="h6">{t('Case Documents')}</Typography>
              <Button variant="outlined" startIcon={<AttachFileIcon />} onClick={handleAddDocument}>
                {t('Add Document')}
              </Button>
            </Box>
            <Grid container spacing={3}>
              {caseData.documents && caseData.documents.length > 0 ? (
                caseData.documents.map((doc, index) => (
                  <Grid item xs={12} sm={6} md={4} key={`doc-${index}`}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <DescriptionIcon sx={{ mr: 1 }} color="primary" />
                          <Typography variant="subtitle1" noWrap>
                            {doc.title}
                          </Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          {doc.description}
                        </Typography>
                        <Box
                          sx={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                          }}
                        >
                          <Typography variant="caption" color="text.secondary">
                            {format(new Date(doc.uploadDate), 'MMM d, yyyy')}
                          </Typography>
                          <Chip label={doc.type} size="small" variant="outlined" />
                        </Box>
                      </CardContent>
                      <CardActions>
                        <Tooltip title={t('Download')}>
                          <IconButton size="small">
                            <DownloadIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title={t('Print')}>
                          <IconButton size="small">
                            <LocalPrintshopIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title={t('Share')}>
                          <IconButton size="small">
                            <ShareIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title={t('Delete')}>
                          <IconButton size="small" color="error">
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                      </CardActions>
                    </Card>
                  </Grid>
                ))
              ) : (
                <Grid item xs={12}>
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="body1" color="text.secondary">
                      {t('No documents attached to this case yet')}
                    </Typography>
                    <Button
                      variant="outlined"
                      startIcon={<AttachFileIcon />}
                      sx={{ mt: 2 }}
                      onClick={handleAddDocument}
                    >
                      {t('Add First Document')}
                    </Button>
                  </Box>
                </Grid>
              )}
            </Grid>
          </Box>
        )}
        {/* Next Steps tab */}
        {tabValue === 3 && (
          <Paper sx={{ p: 3 }}>
            <Box
              sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}
            >
              <Typography variant="h6">{t('Next Steps')}</Typography>
              <Button variant="outlined" startIcon={<MoreTimeIcon />}>
                {t('Add Step')}
              </Button>
            </Box>
            <List>
              {caseData.nextSteps && caseData.nextSteps.length > 0 ? (
                caseData.nextSteps.map((step, index) => (
                  <ListItem
                    key={`step-${index}`}
                    sx={{
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 2,
                    }}
                  >
                    <ListItemIcon>
                      <AccessTimeIcon
                        color={new Date(step.dueDate) < new Date() ? 'error' : 'primary'}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box
                          sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1 }}
                        >
                          <Typography variant="subtitle1">{step.title}</Typography>
                          {step.completed && (
                            <Chip
                              label={t('Completed')}
                              size="small"
                              color="success"
                              icon={<CheckCircleIcon />}
                            />
                          )}
                          {!step.completed && new Date(step.dueDate) < new Date() && (
                            <Chip label={t('Overdue')} size="small" color="error" />
                          )}
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            {step.description}
                          </Typography>
                          <Typography
                            variant="caption"
                            color="text.secondary"
                            sx={{ display: 'block', mt: 1 }}
                          >
                            {t('Due Date')}: {format(new Date(step.dueDate), 'MMM d, yyyy')}
                          </Typography>
                          {step.assignedTo && (
                            <Typography
                              variant="caption"
                              color="text.secondary"
                              sx={{ display: 'block' }}
                            >
                              {t('Assigned to')}: {step.assignedTo}
                            </Typography>
                          )}
                        </>
                      }
                    />
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      {!step.completed && (
                        <Button variant="outlined" size="small" startIcon={<CheckCircleIcon />}>
                          {t('Mark Complete')}
                        </Button>
                      )}
                      <IconButton>
                        <MoreVertIcon />
                      </IconButton>
                    </Box>
                  </ListItem>
                ))
              ) : (
                <Box sx={{ textAlign: 'center', py: 3 }}>
                  <Typography variant="body1" color="text.secondary">
                    {t('No next steps defined for this case')}
                  </Typography>
                  <Button variant="outlined" startIcon={<MoreTimeIcon />} sx={{ mt: 2 }}>
                    {t('Add First Step')}
                  </Button>
                </Box>
              )}
            </List>
          </Paper>
        )}
        {/* Safety Monitor tab */}
        {tabValue === 4 && (
          <Paper sx={{ p: 3 }}>
            <Box
              sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}
            >
              <Typography variant="h6">
                <ShieldIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                {t('Safety Monitor')}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                startIcon={<ShieldIcon />}
                onClick={handleSafetyMonitor}
              >
                {t('Open Safety Monitor')}
              </Button>
            </Box>
            <Box sx={{ my: 2 }}>
              <Typography variant="body1" paragraph>
                {t(
                  'The Safety Monitor feature provides real-time support and safety monitoring for clients in vulnerable situations.'
                )}
              </Typography>
              <Typography variant="body1" paragraph>
                {t(
                  'Features include real-time location sharing, SOS alerts, and direct communication with the support team.'
                )}
              </Typography>
              <Box sx={{ mt: 3, p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  {t('When to use Safety Monitor:')}
                </Typography>
                <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
                  <li>{t('For clients in domestic violence situations')}</li>
                  <li>{t('When clients need real-time support during critical events')}</li>
                  <li>{t('To coordinate emergency interventions with the support team')}</li>
                  <li>{t('For situations requiring location monitoring for client safety')}</li>
                </Typography>
              </Box>
            </Box>
          </Paper>
        )}
      </Container>
    </Box>
  );
};
export default CaseDetailPage;