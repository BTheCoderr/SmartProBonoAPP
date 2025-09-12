import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  InputAdornment,
  Avatar
} from '@mui/material';
import {
  Person as PersonIcon,
  Description as DescriptionIcon,
  CalendarToday as CalendarIcon,
  Gavel as GavelIcon,
  Security as SecurityIcon,
  Payment as PaymentIcon,
  Search as SearchIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Message as MessageIcon
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import PageLayout from '../components/PageLayout';

const BondsmanDashboard = () => {
  const { currentUser } = useAuth();
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [bonds, setBonds] = useState([]);
  const [clients, setClients] = useState([]);
  const [payments, setPayments] = useState([]);
  const [courtDates, setCourtDates] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [paymentForm, setPaymentForm] = useState({
    clientId: '',
    amount: '',
    paymentMethod: 'cash',
    notes: ''
  });
  const [showPaymentForm, setShowPaymentForm] = useState(false);

  // Mock data - in real app, this would come from API
  useEffect(() => {
    const fetchBondsmanData = async () => {
      setLoading(true);
      try {
        // Simulate API calls
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setBonds([
          {
            id: 1,
            clientName: 'John Smith',
            clientPhone: '(555) 123-4567',
            clientEmail: 'john.smith@email.com',
            bondAmount: 25000,
            premium: 2500,
            status: 'Active',
            issueDate: '2024-01-10',
            courtDate: '2024-02-15',
            caseNumber: 'CR-2024-001',
            charges: 'DUI, Reckless Driving',
            courtLocation: 'Providence County Court',
            coSigner: 'Jane Smith (Wife)',
            coSignerPhone: '(555) 123-4568',
            notes: 'First-time offender, good employment history',
            riskLevel: 'Low'
          },
          {
            id: 2,
            clientName: 'Maria Garcia',
            clientPhone: '(555) 234-5678',
            clientEmail: 'maria.garcia@email.com',
            bondAmount: 50000,
            premium: 5000,
            status: 'Forfeited',
            issueDate: '2024-01-05',
            courtDate: '2024-01-20',
            caseNumber: 'CR-2024-002',
            charges: 'Drug Possession, Intent to Distribute',
            courtLocation: 'Kent County Court',
            coSigner: 'Carlos Garcia (Brother)',
            coSignerPhone: '(555) 234-5679',
            notes: 'Failed to appear, bond forfeited',
            riskLevel: 'High'
          },
          {
            id: 3,
            clientName: 'Robert Johnson',
            clientPhone: '(555) 345-6789',
            clientEmail: 'robert.j@email.com',
            bondAmount: 15000,
            premium: 1500,
            status: 'Exonerated',
            issueDate: '2024-01-15',
            courtDate: '2024-01-25',
            caseNumber: 'CR-2024-003',
            charges: 'Theft, Burglary',
            courtLocation: 'Washington County Court',
            coSigner: 'Lisa Johnson (Mother)',
            coSignerPhone: '(555) 345-6790',
            notes: 'Case dismissed, bond exonerated',
            riskLevel: 'Medium'
          }
        ]);

        setClients([
          {
            id: 1,
            name: 'John Smith',
            phone: '(555) 123-4567',
            email: 'john.smith@email.com',
            address: '123 Main St, Providence, RI',
            activeBonds: 1,
            totalBondAmount: 25000,
            lastContact: '2024-01-15',
            status: 'Active'
          },
          {
            id: 2,
            name: 'Maria Garcia',
            phone: '(555) 234-5678',
            email: 'maria.garcia@email.com',
            address: '456 Oak Ave, Warwick, RI',
            activeBonds: 0,
            totalBondAmount: 50000,
            lastContact: '2024-01-20',
            status: 'Forfeited'
          }
        ]);

        setPayments([
          {
            id: 1,
            bondId: 1,
            clientName: 'John Smith',
            amount: 2500,
            paymentDate: '2024-01-10',
            paymentMethod: 'Cash',
            status: 'Completed',
            notes: 'Initial premium payment'
          },
          {
            id: 2,
            bondId: 2,
            clientName: 'Maria Garcia',
            amount: 5000,
            paymentDate: '2024-01-05',
            paymentMethod: 'Check',
            status: 'Completed',
            notes: 'Initial premium payment'
          }
        ]);

        setCourtDates([
          {
            id: 1,
            clientName: 'John Smith',
            caseNumber: 'CR-2024-001',
            courtDate: '2024-02-15',
            time: '9:00 AM',
            location: 'Providence County Court',
            charges: 'DUI, Reckless Driving',
            status: 'Upcoming',
            bondId: 1
          },
          {
            id: 2,
            clientName: 'Robert Johnson',
            caseNumber: 'CR-2024-003',
            courtDate: '2024-01-25',
            time: '2:00 PM',
            location: 'Washington County Court',
            charges: 'Theft, Burglary',
            status: 'Completed',
            bondId: 3
          }
        ]);

      } catch (err) {
        setError('Failed to load bondsman data');
      } finally {
        setLoading(false);
      }
    };

    fetchBondsmanData();
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
    setDialogType('');
    setSelectedItem(null);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active': return 'success';
      case 'Forfeited': return 'error';
      case 'Exonerated': return 'info';
      case 'Pending': return 'warning';
      default: return 'default';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'Low': return 'success';
      case 'Medium': return 'warning';
      case 'High': return 'error';
      default: return 'default';
    }
  };

  const filteredBonds = bonds.filter(bond => {
    const matchesSearch = bond.clientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         bond.caseNumber.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || bond.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const renderBondsTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">Bail Bonds Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog('bond')}
        >
          New Bond
        </Button>
      </Box>

      {/* Search and Filter */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          placeholder="Search bonds..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ flexGrow: 1 }}
        />
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            label="Status"
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="Active">Active</MenuItem>
            <MenuItem value="Forfeited">Forfeited</MenuItem>
            <MenuItem value="Exonerated">Exonerated</MenuItem>
            <MenuItem value="Pending">Pending</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        {filteredBonds.map((bond) => (
          <Grid item xs={12} md={6} lg={4} key={bond.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    {bond.clientName}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip 
                      label={bond.status} 
                      color={getStatusColor(bond.status)}
                      size="small"
                    />
                    <Chip 
                      label={bond.riskLevel} 
                      color={getRiskColor(bond.riskLevel)}
                      size="small"
                    />
                  </Box>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Case: {bond.caseNumber}
                </Typography>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Charges: {bond.charges}
                </Typography>
                
                <Divider sx={{ my: 2 }} />
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Bond Amount: ${bond.bondAmount.toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Premium: ${bond.premium.toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Court Date: {bond.courtDate}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Court: {bond.courtLocation}
                  </Typography>
                </Box>
                
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Co-Signer: {bond.coSigner}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Phone: {bond.coSignerPhone}
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button size="small" startIcon={<EditIcon />}>
                  Edit
                </Button>
                <Button size="small" startIcon={<MessageIcon />}>
                  Contact
                </Button>
                <Button size="small" startIcon={<DescriptionIcon />}>
                  Documents
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderClientsTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Client Management
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Client Name</TableCell>
              <TableCell>Contact</TableCell>
              <TableCell>Active Bonds</TableCell>
              <TableCell>Total Bond Amount</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Last Contact</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {clients.map((client) => (
              <TableRow key={client.id}>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                      <PersonIcon />
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2">{client.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {client.address}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">{client.phone}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {client.email}
                  </Typography>
                </TableCell>
                <TableCell>{client.activeBonds}</TableCell>
                <TableCell>${client.totalBondAmount.toLocaleString()}</TableCell>
                <TableCell>
                  <Chip 
                    label={client.status} 
                    color={getStatusColor(client.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{client.lastContact}</TableCell>
                <TableCell>
                  <IconButton size="small">
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small">
                    <MessageIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );

  const handlePaymentSubmit = (e) => {
    e.preventDefault();
    const newPayment = {
      id: payments.length + 1,
      clientName: clients.find(c => c.id === paymentForm.clientId)?.name || 'Unknown',
      amount: parseFloat(paymentForm.amount),
      paymentDate: new Date().toLocaleDateString(),
      paymentMethod: paymentForm.paymentMethod,
      status: 'Completed',
      notes: paymentForm.notes
    };
    setPayments([...payments, newPayment]);
    setPaymentForm({ clientId: '', amount: '', paymentMethod: 'cash', notes: '' });
    setShowPaymentForm(false);
  };

  const renderPaymentsTab = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">
          Payment Tracking
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setShowPaymentForm(true)}
        >
          Add Payment
        </Button>
      </Box>

      {/* Payment Form Dialog */}
      <Dialog open={showPaymentForm} onClose={() => setShowPaymentForm(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Record New Payment</DialogTitle>
        <form onSubmit={handlePaymentSubmit}>
          <DialogContent>
            <FormControl fullWidth margin="normal">
              <InputLabel>Client</InputLabel>
              <Select
                value={paymentForm.clientId}
                onChange={(e) => setPaymentForm({...paymentForm, clientId: e.target.value})}
                required
              >
                {clients.map((client) => (
                  <MenuItem key={client.id} value={client.id}>
                    {client.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <TextField
              fullWidth
              margin="normal"
              label="Amount"
              type="number"
              value={paymentForm.amount}
              onChange={(e) => setPaymentForm({...paymentForm, amount: e.target.value})}
              InputProps={{
                startAdornment: <InputAdornment position="start">$</InputAdornment>,
              }}
              required
            />
            
            <FormControl fullWidth margin="normal">
              <InputLabel>Payment Method</InputLabel>
              <Select
                value={paymentForm.paymentMethod}
                onChange={(e) => setPaymentForm({...paymentForm, paymentMethod: e.target.value})}
              >
                <MenuItem value="cash">Cash</MenuItem>
                <MenuItem value="check">Check</MenuItem>
                <MenuItem value="credit_card">Credit Card</MenuItem>
                <MenuItem value="bank_transfer">Bank Transfer</MenuItem>
                <MenuItem value="stripe">Stripe (Online)</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              fullWidth
              margin="normal"
              label="Notes"
              multiline
              rows={3}
              value={paymentForm.notes}
              onChange={(e) => setPaymentForm({...paymentForm, notes: e.target.value})}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowPaymentForm(false)}>Cancel</Button>
            <Button type="submit" variant="contained">Record Payment</Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Payment History Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Client</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Payment Date</TableCell>
              <TableCell>Method</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Notes</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {payments.map((payment) => (
              <TableRow key={payment.id}>
                <TableCell>{payment.clientName}</TableCell>
                <TableCell>${payment.amount.toLocaleString()}</TableCell>
                <TableCell>{payment.paymentDate}</TableCell>
                <TableCell>
                  <Chip 
                    label={payment.paymentMethod} 
                    color={payment.paymentMethod === 'Cash' ? 'success' : 'primary'} 
                    size="small" 
                  />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={payment.status} 
                    color={getStatusColor(payment.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{payment.notes}</TableCell>
                <TableCell>
                  <IconButton size="small">
                    <EditIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Payment Summary Cards */}
      <Grid container spacing={2} sx={{ mt: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Payments
              </Typography>
              <Typography variant="h5">
                ${payments.reduce((sum, p) => sum + p.amount, 0).toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                This Month
              </Typography>
              <Typography variant="h5">
                ${payments.filter(p => new Date(p.paymentDate).getMonth() === new Date().getMonth()).reduce((sum, p) => sum + p.amount, 0).toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Payments
              </Typography>
              <Typography variant="h5">
                {payments.filter(p => p.status === 'Pending').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Payment
              </Typography>
              <Typography variant="h5">
                ${payments.length > 0 ? Math.round(payments.reduce((sum, p) => sum + p.amount, 0) / payments.length).toLocaleString() : '0'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderCourtDatesTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Court Dates & Hearings
      </Typography>
      <List>
        {courtDates.map((courtDate) => (
          <ListItem key={courtDate.id} divider>
            <ListItemIcon>
              <GavelIcon color="primary" />
            </ListItemIcon>
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="h6">{courtDate.clientName}</Typography>
                  <Chip 
                    label={courtDate.status} 
                    color={getStatusColor(courtDate.status)}
                    size="small"
                  />
                </Box>
              }
              secondary={
                <Box>
                  <Typography variant="body2">
                    Case: {courtDate.caseNumber} • {courtDate.charges}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {courtDate.courtDate} at {courtDate.time} • {courtDate.location}
                  </Typography>
                </Box>
              }
            />
            <Box sx={{ display: 'flex', gap: 1 }}>
              <IconButton size="small">
                <CalendarIcon />
              </IconButton>
              <IconButton size="small">
                <MessageIcon />
              </IconButton>
            </Box>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const renderDialog = () => (
    <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
      <DialogTitle>
        {dialogType === 'bond' ? 'New Bail Bond' : 'Edit Bond'}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Client Name"
              defaultValue={selectedItem?.clientName || ''}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Client Phone"
              defaultValue={selectedItem?.clientPhone || ''}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Bond Amount"
              type="number"
              defaultValue={selectedItem?.bondAmount || ''}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Premium"
              type="number"
              defaultValue={selectedItem?.premium || ''}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Case Number"
              defaultValue={selectedItem?.caseNumber || ''}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Charges"
              defaultValue={selectedItem?.charges || ''}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Notes"
              multiline
              rows={3}
              defaultValue={selectedItem?.notes || ''}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCloseDialog}>Cancel</Button>
        <Button variant="contained" onClick={handleCloseDialog}>
          {selectedItem ? 'Update' : 'Create'}
        </Button>
      </DialogActions>
    </Dialog>
  );

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <PageLayout
      title="Bondsman Dashboard"
      description="Manage bail bonds, clients, and court dates"
      showBanner={false}
    >
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Bondsman Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Welcome back, {currentUser?.first_name || currentUser?.username}! Manage your bail bond operations.
          </Typography>
        </Box>

        <Paper sx={{ mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} variant="fullWidth">
            <Tab label="Bail Bonds" icon={<SecurityIcon />} />
            <Tab label="Clients" icon={<PersonIcon />} />
            <Tab label="Payments" icon={<PaymentIcon />} />
            <Tab label="Court Dates" icon={<GavelIcon />} />
          </Tabs>
        </Paper>

        <Box sx={{ mt: 3 }}>
          {activeTab === 0 && renderBondsTab()}
          {activeTab === 1 && renderClientsTab()}
          {activeTab === 2 && renderPaymentsTab()}
          {activeTab === 3 && renderCourtDatesTab()}
        </Box>

        {renderDialog()}
      </Container>
    </PageLayout>
  );
};

export default BondsmanDashboard;
