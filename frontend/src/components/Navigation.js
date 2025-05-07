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
  Divider,
  Avatar,
  Menu,
  MenuItem,
  Tooltip
} from '@mui/material';
import { Link, useLocation, useNavigate } from 'react-router-dom';
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
import PersonIcon from '@mui/icons-material/Person';
import LogoutIcon from '@mui/icons-material/Logout';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import SecurityIcon from '@mui/icons-material/Security';
import HistoryEduIcon from '@mui/icons-material/HistoryEdu';
import BusinessIcon from '@mui/icons-material/Business';
import Logo from './Logo';
import Notifications from './Notifications';
import { useAuth } from '../context/AuthContext';

function Navigation() {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const location = useLocation();
  const navigate = useNavigate();
  const { currentUser, isAuthenticated, logout } = useAuth();

  const navItems = [
    { name: 'Home', path: '/', icon: <HomeIcon /> },
    { name: 'Contracts', path: '/contracts', icon: <DescriptionIcon /> },
    { name: 'Immigration', path: '/immigration', icon: <FlightIcon /> },
    { name: 'Expungement', path: '/expungement', icon: <HistoryEduIcon /> },
    { name: 'Documents', path: '/documents', icon: <FolderIcon /> },
    { name: 'Rights', path: '/rights', icon: <GavelIcon /> },
    { name: 'Services', path: '/services', icon: <BuildIcon /> },
    { name: 'Resources', path: '/resources', icon: <LibraryBooksIcon /> },
    { name: 'Business Model', path: '/business-model', icon: <BusinessIcon /> },
    { name: 'Contact', path: '/contact', icon: <ContactSupportIcon /> }
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
    navigate('/login');
  };

  const handleProfile = () => {
    handleMenuClose();
    navigate('/profile');
  };

  const getInitials = () => {
    if (!currentUser) return '?';
    
    if (currentUser.first_name && currentUser.last_name) {
      return `${currentUser.first_name.charAt(0)}${currentUser.last_name.charAt(0)}`;
    } else if (currentUser.username) {
      return currentUser.username.charAt(0).toUpperCase();
    } else {
      return '?';
    }
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
        
        <Divider sx={{ my: 2 }} />
        
        {isAuthenticated ? (
          <>
            <ListItemButton
              component={Link}
              to="/profile"
              selected={location.pathname === '/profile'}
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
                color: location.pathname === '/profile' ? 'white' : 'primary.main'
              }}>
                <PersonIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Profile" 
                primaryTypographyProps={{
                  fontSize: '0.9rem',
                  fontWeight: location.pathname === '/profile' ? 600 : 400
                }}
              />
            </ListItemButton>
            
            <ListItemButton
              onClick={() => {
                logout();
                handleDrawerToggle();
                navigate('/login');
              }}
              sx={{
                borderRadius: 2,
                mb: 1,
              }}
            >
              <ListItemIcon sx={{ 
                minWidth: 40,
                color: 'error.main'
              }}>
                <LogoutIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Logout" 
                primaryTypographyProps={{ 
                  fontSize: '0.9rem',
                  color: 'error.main'
                }}
              />
            </ListItemButton>
          </>
        ) : (
          <>
            <ListItemButton
              component={Link}
              to="/login"
              selected={location.pathname === '/login'}
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
                color: location.pathname === '/login' ? 'white' : 'primary.main'
              }}>
                <LockOpenIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Login" 
                primaryTypographyProps={{
                  fontSize: '0.9rem',
                  fontWeight: location.pathname === '/login' ? 600 : 400
                }}
              />
            </ListItemButton>
            
            <ListItemButton
              component={Link}
              to="/register"
              selected={location.pathname === '/register'}
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
                color: location.pathname === '/register' ? 'white' : 'primary.main'
              }}>
                <AccountCircleIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Register" 
                primaryTypographyProps={{
                  fontSize: '0.9rem',
                  fontWeight: location.pathname === '/register' ? 600 : 400
                }}
              />
            </ListItemButton>
          </>
        )}
      </List>
      </Box>
    );

  return (
    <>
      <AppBar position="fixed" sx={{ bgcolor: 'white', boxShadow: 1 }}>
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
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
              
              <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
                <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center' }}>
                  <Logo variant={isMobile ? "small" : "default"} />
                </Link>
              </Box>

              {!isMobile && (
                <Box sx={{ display: 'flex', gap: 2 }}>
                  {navItems.map((item) => (
                    <Button
                      key={item.name}
                      component={Link}
                      to={item.path}
                      sx={{
                        color: location.pathname === item.path ? 'primary.main' : 'text.primary',
                        '&:hover': {
                          bgcolor: 'rgba(0, 0, 0, 0.04)',
                        },
                      }}
                      startIcon={item.icon}
                    >
                      {item.name}
                    </Button>
                  ))}
                </Box>
              )}

              <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
                {isAuthenticated && <Notifications />}
                
                {isAuthenticated ? (
                  <>
                    <Tooltip title="Account settings">
                      <IconButton
                        onClick={handleMenuOpen}
                        size="small"
                        sx={{ ml: 2 }}
                        aria-controls={open ? 'account-menu' : undefined}
                        aria-haspopup="true"
                        aria-expanded={open ? 'true' : undefined}
                      >
                        <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                          {getInitials()}
                        </Avatar>
                      </IconButton>
                    </Tooltip>
                    <Menu
                      anchorEl={anchorEl}
                      id="account-menu"
                      open={open}
                      onClose={handleMenuClose}
                      onClick={handleMenuClose}
                      transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                      anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                    >
                      <MenuItem onClick={handleProfile}>
                        <ListItemIcon>
                          <PersonIcon fontSize="small" />
                        </ListItemIcon>
                        Profile
                      </MenuItem>
                      <MenuItem onClick={handleLogout}>
                        <ListItemIcon>
                          <LogoutIcon fontSize="small" />
                        </ListItemIcon>
                        Logout
                      </MenuItem>
                    </Menu>
                  </>
                ) : (
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      component={Link}
                      to="/login"
                      variant="outlined"
                      startIcon={<LockOpenIcon />}
                    >
                      Login
                    </Button>
                    <Button
                      component={Link}
                      to="/register"
                      variant="contained"
                      startIcon={<SecurityIcon />}
                    >
                      Register
                    </Button>
                  </Box>
                )}
              </Box>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      
      <Drawer
        variant="temporary"
        anchor="left"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: 280,
            bgcolor: 'background.default'
          },
        }}
      >
        {drawer}
      </Drawer>
      
      <Box component="nav" sx={{ width: { sm: 280 }, flexShrink: { sm: 0 } }} />
    </>
  );
}

export default Navigation;