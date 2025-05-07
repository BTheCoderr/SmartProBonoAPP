import React from 'react';
import { Box, Typography, Grid, Paper, Container, Divider, List, ListItem, ListItemIcon, ListItemText, Card, CardContent } from '@mui/material';
import { styled } from '@mui/material/styles';
import PeopleIcon from '@mui/icons-material/People';
import BusinessIcon from '@mui/icons-material/Business';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import GavelIcon from '@mui/icons-material/Gavel';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import SettingsIcon from '@mui/icons-material/Settings';
import SchoolIcon from '@mui/icons-material/School';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(3),
  color: theme.palette.text.primary,
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
}));

const BusinessModel = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        SmartProBono Business Model
      </Typography>
      
      <Box sx={{ mb: 6 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Our mission is to improve access to legal services through technology
        </Typography>
        <Typography variant="body1" paragraph>
          SmartProBono serves as a platform connecting lawyers with those in need of legal assistance,
          while providing tools to streamline the pro bono process for all parties involved.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Customer Segments */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <PeopleIcon sx={{ mr: 1 }} /> Customer Segments
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <BusinessIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Law Firms" 
                  secondary="Firms looking to fulfill pro bono requirements and improve community standing" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Lawyers" 
                  secondary="Individual attorneys seeking to offer pro bono services efficiently" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <PeopleIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Community" 
                  secondary="Individuals and non-profits seeking affordable legal assistance" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Revenue Streams */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <AttachMoneyIcon sx={{ mr: 1 }} /> Revenue Model
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <AttachMoneyIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Subscription Model" 
                  secondary="Law firms pay a subscription fee for access to the platform" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <AccountBalanceIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Grants" 
                  secondary="Funding from legal foundations and government sources" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <AttachMoneyIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Fee for Potential Clients" 
                  secondary="Optional sliding scale fees for those who can afford some contribution" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Process */}
        <Grid item xs={12}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <SettingsIcon sx={{ mr: 1 }} /> Process
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Free Initial Screening
                  </Typography>
                  <Typography variant="body2">
                    Automated intake process to collect client information and assess legal needs
                  </Typography>
                </CardContent>
              </Card>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                <ArrowForwardIcon sx={{ transform: 'rotate(90deg)' }} />
              </Box>
              
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Case Assignment
                  </Typography>
                  <Typography variant="body2">
                    Matching clients with appropriate lawyers based on expertise and availability
                  </Typography>
                </CardContent>
              </Card>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                <ArrowForwardIcon sx={{ transform: 'rotate(90deg)' }} />
              </Box>
              
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Legal Support
                  </Typography>
                  <Typography variant="body2">
                    Lawyers receive assistance through document templates, AI tools, and case management features
                  </Typography>
                </CardContent>
              </Card>
              
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                <ArrowForwardIcon sx={{ transform: 'rotate(90deg)' }} />
              </Box>
              
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Court Access & Cost Control
                  </Typography>
                  <Typography variant="body2">
                    Tools to navigate court systems efficiently while controlling costs
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          </Item>
        </Grid>

        {/* Strategic Focus */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <SchoolIcon sx={{ mr: 1 }} /> Narrowing Focus
            </Typography>
            <Typography variant="body1" paragraph>
              Instead of providing general legal services, SmartProBono is focusing on specific practice areas:
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText primary="Immigration Law" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText primary="Landlord-Tenant Issues" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText primary="Family Law" />
              </ListItem>
            </List>
          </Item>
        </Grid>

        {/* Lawyer Benefits */}
        <Grid item xs={12} md={6}>
          <Item>
            <Typography variant="h5" component="h2" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <GavelIcon sx={{ mr: 1 }} /> For Lawyers
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Referral System" 
                  secondary="Efficient matching of cases to appropriate legal expertise" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Case Management" 
                  secondary="Tools to manage pro bono cases alongside regular workload" 
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <GavelIcon />
                </ListItemIcon>
                <ListItemText 
                  primary="Client Updates" 
                  secondary="Streamlined communication with pro bono clients" 
                />
              </ListItem>
            </List>
          </Item>
        </Grid>
      </Grid>
    </Container>
  );
};

export default BusinessModel; 