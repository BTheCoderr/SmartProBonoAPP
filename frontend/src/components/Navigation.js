import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Button, 
  Typography, 
  Box,
  Container,
  IconButton,
  Drawer,
  List,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  useTheme,
  useMediaQuery,
  Divider
} from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import DescriptionIcon from '@mui/icons-material/Description';
import GavelIcon from '@mui/icons-material/Gavel';
import ChatIcon from '@mui/icons-material/Chat';
import FlightIcon from '@mui/icons-material/Flight';
import BuildIcon from '@mui/icons-material/Build';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import ContactSupportIcon from '@mui/icons-material/ContactSupport';
import FolderIcon from '@mui/icons-material/Folder';
import Logo from './Logo';

function Navigation() {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const location = useLocation();

  const navItems = [
    { name: 'Home', path: '/', icon: <HomeIcon /> },
    { name: 'Contracts', path: '/services/contracts', icon: <DescriptionIcon /> },
    { name: 'Rights', path: '/resources/rights', icon: <GavelIcon /> },
    { name: 'Immigration', path: '/services/immigration', icon: <FlightIcon /> },
    { name: 'Documents', path: '/documents', icon: <FolderIcon /> },
    { name: 'Services', path: '/services', icon: <BuildIcon /> },
    { name: 'Resources', path: '/resources', icon: <LibraryBooksIcon /> },
    { name: 'Contact', path: '/contact', icon: <ContactSupportIcon /> }
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box sx={{ bgcolor: '#fff', height: '100%' }}>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', borderBottom: 1, borderColor: 'divider' }}>
        <Logo variant="small" />
      </Box>
      <List sx={{ p: 2 }}>
        {navItems.map((item) => (
          <ListItemButton
            key={item.name}
            component={Link}
            to={item.path}
            selected={location.pathname === item.path}
            onClick={handleDrawerToggle}
            sx={{
              borderRadius: 2,
              mb: 1,
              '&.Mui-selected': {
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
                '& .MuiListItemIcon-root': {
                  color: 'white',
                }
              },
            }}
          >
            <ListItemIcon sx={{ 
              minWidth: 40,
              color: location.pathname === item.path ? 'white' : 'primary.main'
            }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText 
              primary={item.name} 
              primaryTypographyProps={{
                fontSize: '0.9rem',
                fontWeight: location.pathname === item.path ? 600 : 400
              }}
            />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar 
        position="fixed" 
        elevation={0}
        sx={{ 
          bgcolor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(8px)',
          borderBottom: '1px solid',
          borderColor: 'divider',
          py: 0.5
        }}
      >
        <Container maxWidth="xl">
          <Toolbar sx={{ px: { xs: 1, sm: 2 }, minHeight: '64px' }}>
            {isMobile && (
              <IconButton
                color="primary"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
            )}
            
            <Box 
              component={Link} 
              to="/"
              sx={{ 
                textDecoration: 'none',
                color: 'primary.main',
                display: 'flex',
                alignItems: 'center',
                mr: 3,
                minWidth: { xs: 'auto', md: '200px' }
              }}
            >
              <Logo variant="light" size={isMobile ? "small" : "medium"} />
            </Box>

            {!isMobile && (
              <Box sx={{ 
                display: 'flex', 
                gap: 1,
                flexGrow: 1,
                justifyContent: 'center'
              }}>
                {navItems.map((item) => (
                  <Button
                    key={item.name}
                    component={Link}
                    to={item.path}
                    color="primary"
                    startIcon={item.icon}
                    sx={{
                      px: 1.5,
                      py: 1,
                      minWidth: 'auto',
                      borderRadius: 2,
                      textTransform: 'none',
                      fontSize: '0.9rem',
                      fontWeight: location.pathname === item.path ? 600 : 400,
                      bgcolor: location.pathname === item.path ? 'primary.main' : 'transparent',
                      color: location.pathname === item.path ? 'white' : 'primary.main',
                      transition: 'all 0.2s ease-in-out',
                      '&:hover': {
                        bgcolor: location.pathname === item.path ? 'primary.dark' : 'rgba(25, 118, 210, 0.08)',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                      }
                    }}
                  >
                    {item.name}
                  </Button>
                ))}
              </Box>
            )}

            <Box sx={{ ml: 2 }}>
              <Button
                variant="contained"
                component={Link}
                to="/legal-chat"
                startIcon={<ChatIcon />}
                sx={{
                  display: { xs: 'none', sm: 'flex' },
                  borderRadius: 2,
                  textTransform: 'none',
                  px: 2,
                  py: 1,
                  fontSize: '0.9rem',
                  fontWeight: 500,
                  boxShadow: 'none',
                  background: 'linear-gradient(45deg, #1976d2 30%, #2196f3 90%)',
                  transition: 'all 0.2s ease-in-out',
                  '&:hover': {
                    boxShadow: '0 2px 8px rgba(33, 150, 243, .3)',
                    transform: 'translateY(-2px)'
                  }
                }}
              >
                Legal Chat
              </Button>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      <Toolbar /> {/* Spacer for fixed AppBar */}

      <Drawer
        variant="temporary"
        anchor="left"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: 280
          },
        }}
      >
        {drawer}
      </Drawer>
    </Box>
  );
}

export default Navigation;