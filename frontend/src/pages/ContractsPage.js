import React, { useState, useEffect, useMemo } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  Chip, 
  Divider,
  IconButton,
  Stack,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { motion } from 'framer-motion';
import { 
  PageLayout, 
  Section, 
  Button, 
  Card, 
  CardContent,
  designTokens 
} from '../design-system';
import DescriptionIcon from '@mui/icons-material/Description';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import ShareIcon from '@mui/icons-material/Share';
import BusinessIcon from '@mui/icons-material/Business';
import WorkIcon from '@mui/icons-material/Work';
import SecurityIcon from '@mui/icons-material/Security';
import AssignmentIcon from '@mui/icons-material/Assignment';
import GavelIcon from '@mui/icons-material/Gavel';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import ContractTemplateService from '../services/ContractTemplateService';
import ContractForm from '../components/ContractForm';
import ContractPreview from '../components/ContractPreview';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`contracts-tabpanel-${index}`}
      aria-labelledby={`contracts-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: designTokens.spacing[6] }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const ContractsPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [myContracts, setMyContracts] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [previewContract, setPreviewContract] = useState(null);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Sample user contracts data
  const userContracts = useMemo(() => [
    {
      id: 1,
      name: 'Employment Contract - John Smith',
      type: 'Employment Agreement',
      status: 'Draft',
      createdDate: '2024-01-15',
      lastModified: '2024-01-16',
    },
    {
      id: 2,
      name: 'NDA - Tech Startup',
      type: 'Non-Disclosure Agreement',
      status: 'Review',
      createdDate: '2024-01-10',
      lastModified: '2024-01-14',
    },
    {
      id: 3,
      name: 'Service Agreement - Client ABC',
      type: 'Service Agreement',
      status: 'Signed',
      createdDate: '2024-01-05',
      lastModified: '2024-01-12',
    },
  ], []); // Empty dependency array since this is static data

  // Load user contracts on component mount
  useEffect(() => {
    const contracts = ContractTemplateService.getUserContracts();
    // If no contracts from service, use the sample data
    if (contracts.length === 0) {
      setMyContracts(userContracts);
    } else {
      setMyContracts(contracts);
    }
  }, [userContracts]); // Include userContracts dependency

  const handleUseTemplate = (template) => {
    setSelectedTemplate(template);
    setShowForm(true);
  };

  const handleFormSave = (savedContract) => {
    setMyContracts(prev => [savedContract, ...prev]);
    setRecentActivity(prev => [{
      id: Date.now(),
      action: 'Created',
      contract: savedContract.name,
      timestamp: new Date().toLocaleTimeString(),
    }, ...prev]);
    
    setShowForm(false);
    setSelectedTemplate(null);
    
    // Show success message
    alert(`Contract "${savedContract.name}" created successfully! Check "My Contracts" tab.`);
  };

  const handleFormPreview = (contract) => {
    setPreviewContract(contract);
    setShowPreview(true);
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setSelectedTemplate(null);
  };

  const handlePreviewClose = () => {
    setShowPreview(false);
    setPreviewContract(null);
  };

  const handlePreviewEdit = () => {
    setShowPreview(false);
    setPreviewContract(null);
    // Keep form open for editing
  };

  const handlePreviewDownload = () => {
    // TODO: Implement PDF generation and download
    alert('PDF download functionality will be implemented with the signature system');
  };

  const handleCreateNewContract = () => {
    setTabValue(1); // Switch to Templates tab
  };

  const handleBrowseTemplates = () => {
    setTabValue(1); // Switch to Templates tab
  };

  // Get templates from service
  const contractTemplates = ContractTemplateService.getAllTemplates().map(template => ({
    ...template,
    icon: getTemplateIcon(template.id)
  }));

  // Helper function to get icon for template
  function getTemplateIcon(templateId) {
    switch (templateId) {
      case 'employment': return <WorkIcon />;
      case 'nda': return <SecurityIcon />;
      case 'service': return <BusinessIcon />;
      case 'partnership': return <AssignmentIcon />;
      case 'lease': return <GavelIcon />;
      case 'consulting': return <TrendingUpIcon />;
      default: return <DescriptionIcon />;
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'Complete': return 'success';
      case 'Review': return 'warning';
      case 'Draft': return 'info';
      default: return 'default';
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'Employment': return 'primary';
      case 'Business': return 'secondary';
      case 'Real Estate': return 'success';
      default: return 'default';
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  return (
    <PageLayout background="light" padding="normal">
      {/* Hero Section */}
      <Section variant="hero" background="gradient" header={false}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <Box sx={{ textAlign: 'center', py: designTokens.spacing[8] }}>
            <motion.div variants={itemVariants}>
              <Box
                sx={{
                  width: 100,
                  height: 100,
                  borderRadius: '50%',
                  background: 'rgba(255, 255, 255, 0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto',
                  mb: designTokens.spacing[6],
                  backdropFilter: 'blur(10px)',
                }}
              >
                <DescriptionIcon sx={{ fontSize: 50, color: 'white' }} />
              </Box>
              <Typography
                variant="h2"
                sx={{
                  fontWeight: designTokens.typography.fontWeight.bold,
                  color: 'white',
                  mb: designTokens.spacing[4],
                  textShadow: '0 2px 8px rgba(0,0,0,0.3)',
                }}
              >
                Contract Templates
              </Typography>
              <Typography
                variant="h5"
                sx={{
                  color: 'rgba(255, 255, 255, 0.9)',
                  mb: designTokens.spacing[6],
                  textShadow: '0 1px 4px rgba(0,0,0,0.3)',
                  maxWidth: '600px',
                  margin: '0 auto',
                }}
              >
                Create professional legal contracts with our AI-powered templates. 
                Free, customizable, and legally compliant.
              </Typography>
              <Stack
                direction={{ xs: 'column', sm: 'row' }}
                spacing={designTokens.spacing[4]}
                justifyContent="center"
                sx={{ mt: designTokens.spacing[6] }}
              >
                <Button
                  variant="primary"
                  size="large"
                  startIcon={<AddIcon />}
                  onClick={handleCreateNewContract}
                  sx={{
                    backgroundColor: 'white',
                    color: '#0D47A1', // Dark blue for better contrast
                    fontWeight: 700,
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.9)',
                      boxShadow: '0 6px 20px rgba(0, 0, 0, 0.2)',
                      transform: 'translateY(-2px)',
                    },
                  }}
                >
                  Create New Contract
                </Button>
                <Button
                  variant="secondary"
                  size="large"
                  startIcon={<DescriptionIcon />}
                  onClick={handleBrowseTemplates}
                  sx={{
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    color: 'white',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                >
                  Browse Templates
                </Button>
              </Stack>
            </motion.div>
          </Box>
        </motion.div>
      </Section>

      {/* Main Content */}
      <Section variant="default" background="white" header={false}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <Card variant="elevated" sx={{ p: designTokens.spacing[6] }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              sx={{
                borderBottom: 1,
                borderColor: 'divider',
                mb: designTokens.spacing[6],
              }}
            >
              <Tab label="Templates" />
              <Tab label="My Contracts" />
              <Tab label="Recent Activity" />
            </Tabs>

            {/* Templates Tab */}
            <TabPanel value={tabValue} index={0}>
              <Grid container spacing={designTokens.spacing[6]}>
                {contractTemplates.map((template, index) => (
                  <Grid item xs={12} md={6} lg={4} key={template.id}>
                    <motion.div variants={itemVariants}>
                      <Card
                        variant="default"
                        hoverable
                        sx={{
                          height: '100%',
                          position: 'relative',
                          '&:hover': {
                            transform: 'translateY(-4px)',
                          },
                        }}
                      >
                        {template.popular && (
                          <Chip
                            label="Popular"
                            color="primary"
                            size="small"
                            sx={{
                              position: 'absolute',
                              top: designTokens.spacing[3],
                              right: designTokens.spacing[3],
                              zIndex: 1,
                            }}
                          />
                        )}
                        <CardContent sx={{ p: designTokens.spacing[6] }}>
                          <Box
                            sx={{
                              display: 'flex',
                              alignItems: 'center',
                              mb: designTokens.spacing[4],
                            }}
                          >
                            <Box
                              sx={{
                                width: 50,
                                height: 50,
                                borderRadius: '50%',
                                background: designTokens.gradients.primary,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                mr: designTokens.spacing[3],
                              }}
                            >
                              {React.cloneElement(template.icon, { 
                                sx: { fontSize: 24, color: 'white' } 
                              })}
                            </Box>
                            <Box>
                              <Chip
                                label={template.category}
                                color={getCategoryColor(template.category)}
                                size="small"
                                sx={{ mb: designTokens.spacing[1] }}
                              />
                              <Typography
                                variant="h6"
                                sx={{
                                  fontWeight: designTokens.typography.fontWeight.bold,
                                  color: designTokens.colors.neutral[800],
                                }}
                              >
                                {template.title}
                              </Typography>
                            </Box>
                          </Box>

                          <Typography
                            variant="body2"
                            color="text.secondary"
                            sx={{ mb: designTokens.spacing[4] }}
                          >
                            {template.description}
                          </Typography>

                          <Box sx={{ mb: designTokens.spacing[4] }}>
                            <Typography
                              variant="subtitle2"
                              sx={{
                                fontWeight: designTokens.typography.fontWeight.semibold,
                                mb: designTokens.spacing[2],
                                color: designTokens.colors.neutral[700],
                              }}
                            >
                              Features:
                            </Typography>
                            <Stack direction="row" spacing={1} flexWrap="wrap">
                              {template.features.map((feature, idx) => (
                                <Chip
                                  key={idx}
                                  label={feature}
                                  size="small"
                                  variant="outlined"
                                  sx={{
                                    fontSize: '0.75rem',
                                    height: 24,
                                    mb: designTokens.spacing[1],
                                  }}
                                />
                              ))}
                            </Stack>
                          </Box>

                          <Box
                            sx={{
                              display: 'flex',
                              justifyContent: 'space-between',
                              alignItems: 'center',
                            }}
                          >
                            <Typography
                              variant="h6"
                              sx={{
                                fontWeight: designTokens.typography.fontWeight.bold,
                                color: designTokens.colors.success[600],
                              }}
                            >
                              {template.price}
                            </Typography>
                            <Button
                              variant="primary"
                              size="small"
                              startIcon={<AddIcon />}
                              onClick={() => handleUseTemplate(template)}
                              sx={{
                                backgroundColor: '#1565C0',
                                color: 'white',
                                fontWeight: 600,
                                '&:hover': {
                                  backgroundColor: '#0D47A1',
                                  transform: 'translateY(-1px)',
                                },
                              }}
                            >
                              Use Template
                            </Button>
                          </Box>
                        </CardContent>
                      </Card>
                    </motion.div>
                  </Grid>
                ))}
              </Grid>
            </TabPanel>

            {/* My Contracts Tab */}
            <TabPanel value={tabValue} index={1}>
              <motion.div variants={itemVariants}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    mb: designTokens.spacing[6],
                  }}
                >
                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: designTokens.typography.fontWeight.bold,
                      color: designTokens.colors.neutral[800],
                    }}
                  >
                    My Contracts
                  </Typography>
                  <Button
                    variant="primary"
                    startIcon={<AddIcon />}
                  >
                    Create New
                  </Button>
                </Box>

                <List>
                  {myContracts.length === 0 ? (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="h6" color="text.secondary" gutterBottom>
                        No contracts yet
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Use a template to create your first contract
                      </Typography>
                    </Box>
                  ) : (
                    myContracts.map((contract, index) => (
                    <React.Fragment key={contract.id}>
                      <ListItem
                        sx={{
                          p: designTokens.spacing[4],
                          borderRadius: designTokens.borderRadius.md,
                          '&:hover': {
                            backgroundColor: designTokens.colors.neutral[50],
                          },
                        }}
                      >
                        <ListItemIcon>
                          <DescriptionIcon sx={{ color: designTokens.colors.primary[500] }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="h6" sx={{ fontWeight: designTokens.typography.fontWeight.semibold }}>
                              {contract.title}
                            </Typography>
                          }
                          secondary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: designTokens.spacing[2], mt: designTokens.spacing[1] }}>
                              <Chip
                                label={contract.type}
                                size="small"
                                variant="outlined"
                                sx={{ fontSize: '0.75rem' }}
                              />
                              <Chip
                                label={contract.status}
                                size="small"
                                color={getStatusColor(contract.status)}
                                sx={{ fontSize: '0.75rem' }}
                              />
                              <Typography variant="caption" color="text.secondary">
                                Created: {contract.createdDate}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                Modified: {contract.lastModified}
                              </Typography>
                            </Box>
                          }
                        />
                        <Box sx={{ display: 'flex', gap: designTokens.spacing[1] }}>
                          <IconButton size="small">
                            <EditIcon />
                          </IconButton>
                          <IconButton size="small">
                            <DownloadIcon />
                          </IconButton>
                          <IconButton size="small">
                            <ShareIcon />
                          </IconButton>
                          <IconButton size="small" color="error">
                            <DeleteIcon />
                          </IconButton>
                        </Box>
                      </ListItem>
                      {index < myContracts.length - 1 && <Divider />}
                    </React.Fragment>
                    ))
                  )}
                </List>
              </motion.div>
            </TabPanel>

            {/* Recent Activity Tab */}
            <TabPanel value={tabValue} index={2}>
              <motion.div variants={itemVariants}>
                <Typography
                  variant="h5"
                  sx={{
                    fontWeight: designTokens.typography.fontWeight.bold,
                    color: designTokens.colors.neutral[800],
                    mb: designTokens.spacing[6],
                  }}
                >
                  Recent Activity
                </Typography>
                {recentActivity.length === 0 ? (
                  <Box sx={{ textAlign: 'center', py: designTokens.spacing[8] }}>
                    <DescriptionIcon sx={{ fontSize: 64, color: designTokens.colors.neutral[300], mb: designTokens.spacing[4] }} />
                    <Typography variant="h6" color="text.secondary" sx={{ mb: designTokens.spacing[2] }}>
                      No recent activity
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Your contract activity will appear here
                    </Typography>
                  </Box>
                ) : (
                  <List>
                    {recentActivity.map((activity, index) => (
                      <React.Fragment key={activity.id}>
                        <ListItem
                          sx={{
                            p: designTokens.spacing[3],
                            borderRadius: designTokens.borderRadius.md,
                            '&:hover': {
                              backgroundColor: designTokens.colors.neutral[50],
                            },
                          }}
                        >
                          <ListItemIcon>
                            <AddIcon sx={{ color: designTokens.colors.success[500] }} />
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Typography variant="h6" sx={{ fontWeight: designTokens.typography.fontWeight.semibold }}>
                                {activity.type}
                              </Typography>
                            }
                            secondary={
                              <React.Fragment>
                                <Typography component="span" variant="body2" color="text.secondary" display="block">
                                  {activity.description}
                                </Typography>
                                <Typography component="span" variant="caption" color="text.secondary">
                                  {new Date(activity.timestamp).toLocaleString()}
                                </Typography>
                              </React.Fragment>
                            }
                          />
                        </ListItem>
                        {index < recentActivity.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                )}
              </motion.div>
            </TabPanel>
          </Card>
        </motion.div>
      </Section>

      {/* Contract Form Dialog */}
      <Dialog
        open={showForm}
        onClose={handleFormCancel}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            minHeight: '80vh',
          }
        }}
      >
        <DialogTitle>
          {selectedTemplate ? `Create ${selectedTemplate.name}` : 'Create Contract'}
        </DialogTitle>
        <DialogContent sx={{ p: 0 }}>
          {selectedTemplate && (
            <ContractForm
              templateId={selectedTemplate.id}
              onSave={handleFormSave}
              onPreview={handleFormPreview}
              onCancel={handleFormCancel}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleFormCancel}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Contract Preview Dialog */}
      <Dialog
        open={showPreview}
        onClose={handlePreviewClose}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            minHeight: '90vh',
          }
        }}
      >
        <DialogTitle>Contract Preview</DialogTitle>
        <DialogContent sx={{ p: 0 }}>
          {previewContract && (
            <ContractPreview
              contract={previewContract}
              onEdit={handlePreviewEdit}
              onDownload={handlePreviewDownload}
              onClose={handlePreviewClose}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handlePreviewClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </PageLayout>
  );
};

export default ContractsPage;