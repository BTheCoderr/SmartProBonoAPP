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
    { name: 'Home', path: '/', icon: <HomeIcon />, isPrimary: false },
    { name: 'Legal AI Chat', path: '/legal-chat', icon: <ChatIcon />, isPrimary: true },
    { name: 'Documents', path: '/documents', icon: <FolderIcon />, isPrimary: true },
    { name: 'Forms Dashboard', path: '/forms-dashboard', icon: <DescriptionIcon />, isPrimary: true },
    { name: 'Virtual Paralegal', path: '/virtual-paralegal', icon: <GavelIcon />, isPrimary: true },
    { name: 'Resources', path: '/resources', icon: <LibraryBooksIcon />, isPrimary: true },
    { name: 'Immigration', path: '/immigration', icon: <FlightIcon />, isPrimary: false },
    { name: 'Expungement', path: '/expungement', icon: <HistoryEduIcon />, isPrimary: false },
    { name: 'Rights', path: '/rights', icon: <GavelIcon />, isPrimary: false },
    { name: 'Services', path: '/services', icon: <BuildIcon />, isPrimary: false },
    { name: 'Contact', path: '/contact', icon: <ContactSupportIcon />, isPrimary: false }
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
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            <Box sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }}>
              <Logo variant="small" />
            </Box>

            <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
              >
                <MenuIcon />
              </IconButton>
            </Box>

            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, gap: 2 }}>
              {navItems.filter(item => item.isPrimary).map((item) => (
                <Button
                  key={item.name}
                  component={Link}
                  to={item.path}
                  sx={{
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.5,
                    '&:hover': {
                      bgcolor: 'primary.dark',
                    },
                  }}
                  startIcon={item.icon}
                >
                  {item.name}
                </Button>
              ))}
            </Box>

            {!isAuthenticated && (
              <Button
                variant="contained"
                color="secondary"
                component={Link}
                to="/legal-chat"
                sx={{
                  mr: 2,
                  fontWeight: 600,
                  boxShadow: 2,
                  '&:hover': {
                    boxShadow: 4,
                  },
                }}
              >
                Get Started
              </Button>
            )}

            <Box sx={{ flexGrow: 0 }}>
              {isAuthenticated ? (
                <>
                  <Notifications />
                  <Tooltip title="Open settings">
                    <IconButton onClick={handleMenuOpen} sx={{ p: 0, ml: 2 }}>
                      <Avatar sx={{ bgcolor: 'secondary.main' }}>
                        {getInitials()}
                      </Avatar>
                    </IconButton>
                  </Tooltip>
                </>
              ) : (
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    component={Link}
                    to="/login"
                    color="inherit"
                    startIcon={<LockOpenIcon />}
                  >
                    Login
                  </Button>
                </Box>
              )}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        sx={{ mt: '45px' }}
      >
        <MenuItem onClick={handleProfile}>
          <ListItemIcon>
            <AccountCircleIcon fontSize="small" />
          </ListItemIcon>
          <Typography textAlign="center">Profile</Typography>
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <LogoutIcon fontSize="small" color="error" />
          </ListItemIcon>
          <Typography textAlign="center" color="error">Logout</Typography>
        </MenuItem>
      </Menu>

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
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 280 },
        }}
      >
        {drawer}
      </Drawer>
    </>
  );
}

export default Navigation;