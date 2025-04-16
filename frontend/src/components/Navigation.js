import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Button,
  Typography,
  Box,
  Container,
  IconButton,
  List,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  useTheme,
  useMediaQuery,
  Divider,
  Tooltip,
  Avatar,
  SwipeableDrawer,
  Menu,
  MenuItem,
  Chip,
} from '@mui/material';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import DescriptionIcon from '@mui/icons-material/Description';
import GavelIcon from '@mui/icons-material/Gavel';
import ChatIcon from '@mui/icons-material/Chat';
import FlightIcon from '@mui/icons-material/Flight';
import BuildIcon from '@mui/icons-material/Build';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import ContactSupportIcon from '@mui/icons-material/ContactSupport';
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import CloseIcon from '@mui/icons-material/Close';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import CallIcon from '@mui/icons-material/Call';
import FolderIcon from '@mui/icons-material/Folder';
import LoginIcon from '@mui/icons-material/Login';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import Logo from '../components/Logo';
import LanguageSelector from './LanguageSelector';
import NotificationCenter from './NotificationCenter';
import { useAuth } from '../contexts/AuthContext';

function Navigation() {
  const { t } = useTranslation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [highContrast, setHighContrast] = useState(false);
  const [userMenuAnchor, setUserMenuAnchor] = useState(null);
  
  // Use the Auth context instead of local state
  const { isAuthenticated, user } = useAuth();

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const location = useLocation();
  const navigate = useNavigate();

  // Handle scroll effect for AppBar
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Always visible navigation items
  const publicNavItems = [
    { name: 'Home', path: '/', icon: <HomeIcon />, ariaLabel: 'Go to home page' },
    {
      name: 'Find Lawyer',
      path: '/find-lawyer',
      icon: <GavelIcon />,
      ariaLabel: 'Find a pro bono lawyer',
    },
    {
      name: 'Rights',
      path: '/resources/rights',
      icon: <GavelIcon />,
      ariaLabel: 'Know your rights',
    },
    {
      name: 'Immigration',
      path: '/services/immigration',
      icon: <FlightIcon />,
      ariaLabel: 'Immigration help',
    },
    {
      name: 'Services',
      path: '/services',
      icon: <BuildIcon />,
      ariaLabel: 'Go to services page',
      requiresAuth: true,
    },
    {
      name: 'Resources',
      path: '/resources',
      icon: <LibraryBooksIcon />,
      ariaLabel: 'Go to resources page',
      requiresAuth: true,
    },
    {
      name: 'Accessibility',
      path: '/accessibility',
      icon: <AccessibilityNewIcon />,
      ariaLabel: 'Accessibility features',
    },
    {
      name: 'Contact',
      path: '/contact',
      icon: <ContactSupportIcon />,
      ariaLabel: 'Go to contact page',
    },
    {
      name: 'Emergency Support',
      path: '/emergency-support',
      icon: <CallIcon color="error" />,
      ariaLabel: 'Get emergency legal support',
      highlight: true,
    },
  ];

  // Only visible when authenticated
  const authOnlyNavItems = [
    {
      name: 'Document Templates',
      path: '/document-templates',
      icon: <DescriptionIcon />,
      ariaLabel: 'Go to document templates page',
    },
    {
      name: 'Case Management',
      path: '/cases',
      icon: <FolderIcon />,
      ariaLabel: 'Go to case management',
      isNew: true,
    },
    {
      name: 'Document Analyzer',
      path: '/document-analyzer',
      icon: <AnalyticsIcon />,
      ariaLabel: 'Go to document analyzer page',
    },
    {
      name: 'Settings',
      path: '/settings',
      icon: <SettingsIcon />,
      ariaLabel: 'Go to settings page',
    },
  ];

  // Filtering nav items for display
  const allNavItems = [...publicNavItems, ...authOnlyNavItems];

  // Get items for the drawer (mobile menu)
  const drawerNavItems = allNavItems.filter(
    item => !item.requiresAuth || (item.requiresAuth && isAuthenticated)
  );

  // Get items for the desktop menu (top bar)
  const desktopNavItems = publicNavItems.filter(
    item => !item.requiresAuth || (item.requiresAuth && isAuthenticated)
  );

  // Languages are now handled by the LanguageSelector component
  const accessibilityOptions = [
    { name: 'High Contrast Mode', action: () => setHighContrast(!highContrast) },
    { name: 'Increase Font Size', action: () => (document.body.style.fontSize = '1.2em') },
    { name: 'Reset Font Size', action: () => (document.body.style.fontSize = '1em') },
    {
      name: 'Accessibility Settings',
      action: () => {
        navigate('/accessibility');
        handleAccessibilityClose();
      },
    },
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // Add a new method to close the drawer when navigating on mobile
  const handleNavigation = (path) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  // Language selection is now handled by the LanguageSelector component

  const handleAccessibilityClick = () => {
    navigate('/accessibility');
  };

  const handleAccessibilityClose = () => {
    setHighContrast(false);
  };

  const handleUserMenuClick = (event) => {
    setUserMenuAnchor(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setUserMenuAnchor(null);
  };

  const handleLogout = () => {
    // Implement logout logic here
    handleUserMenuClose();
    navigate('/login');
  };

  // Improve the navigation drawer rendering for mobile
  const renderDrawer = () => {
    return (
      <Box
        onClick={isMobile ? handleDrawerToggle : undefined}
        sx={{
          width: { xs: '100%', sm: 280 },
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            p: 2,
            borderBottom: 1,
            borderColor: 'divider',
          }}
        >
          <Logo height={40} />
          <IconButton 
            onClick={handleDrawerToggle} 
            sx={{ display: { sm: 'none' } }}
            edge="end"
          >
            <CloseIcon />
          </IconButton>
        </Box>

        <List sx={{ flexGrow: 1, pt: 0 }}>
          {drawerNavItems.map((item) => (
            <ListItemButton
              key={item.path}
              onClick={() => handleNavigation(item.path)}
              selected={location.pathname === item.path}
              sx={{
                py: 1.5,
                px: 3,
                borderRadius: 0,
                mb: 0.5,
                '&.Mui-selected': {
                  backgroundColor: (theme) => 
                    theme.palette.mode === 'dark' 
                      ? 'rgba(255, 255, 255, 0.08)'
                      : 'rgba(25, 118, 210, 0.08)',
                  borderLeft: 3,
                  borderColor: 'primary.main',
                  '&:hover': {
                    backgroundColor: (theme) => 
                      theme.palette.mode === 'dark' 
                        ? 'rgba(255, 255, 255, 0.12)'
                        : 'rgba(25, 118, 210, 0.12)',
                  },
                },
                '&:hover': {
                  backgroundColor: (theme) => 
                    theme.palette.mode === 'dark' 
                      ? 'rgba(255, 255, 255, 0.08)'
                      : 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 40,
                  color: location.pathname === item.path ? 'primary.main' : 'text.secondary',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={t(item.name)} 
                primaryTypographyProps={{ 
                  fontSize: '0.95rem',
                  fontWeight: location.pathname === item.path ? 600 : 400,
                }}
              />
              {item.isNew && (
                <Chip
                  label={t('New')}
                  size="small"
                  color="secondary"
                  sx={{ ml: 1, height: 20, fontSize: '0.625rem' }}
                />
              )}
              {item.highlight && (
                <Chip
                  label={t('SOS')}
                  size="small"
                  color="error"
                  sx={{ ml: 1, height: 20, fontSize: '0.625rem' }}
                />
              )}
            </ListItemButton>
          ))}
        </List>

        {isAuthenticated && (
          <Box
            sx={{
              p: 2,
              borderTop: 1,
              borderColor: 'divider',
              display: 'flex',
              flexDirection: 'column',
              gap: 1,
            }}
          >
            <Button
              variant="outlined"
              color="inherit"
              startIcon={<SettingsIcon />}
              fullWidth
              onClick={() => handleNavigation('/settings')}
              sx={{ justifyContent: 'flex-start', px: 2 }}
            >
              {t('Settings')}
            </Button>
            <Button
              variant="contained"
              color="primary"
              startIcon={<ExitToAppIcon />}
              fullWidth
              onClick={handleLogout}
              sx={{ justifyContent: 'flex-start', px: 2 }}
            >
              {t('Logout')}
            </Button>
          </Box>
        )}
      </Box>
    );
  };

  return (
    <>
      <AppBar 
        position="fixed" 
        sx={{ 
          width: '100%',
          left: 0,
          backgroundColor: theme.palette.background.paper,
          boxShadow: scrolled ? 1 : 0,
          borderBottom: !scrolled ? '1px solid rgba(0, 0, 0, 0.12)' : 'none',
        }}
      >
        <Container maxWidth={false} sx={{ width: '100%', px: { xs: 2, sm: 3 } }}>
          <Toolbar disableGutters>
            <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ mr: 2, display: { md: 'none' } }}
              >
                <MenuIcon />
              </IconButton>
              
              <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Logo size="small" variant={highContrast ? 'highContrast' : 'light'} />
                </Box>
              </Link>
            </Box>

            {/* Main Navigation (Desktop) */}
            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, ml: 2 }}>
              {desktopNavItems.map(item => (
                <Button
                  key={item.name}
                  component={Link}
                  to={item.requiresAuth && !isAuthenticated ? '/login' : item.path}
                  state={item.requiresAuth && !isAuthenticated ? { from: item.path } : undefined}
                  aria-label={item.ariaLabel}
                  startIcon={item.icon}
                  color={item.highlight ? 'error' : 'inherit'}
                  sx={{
                    mx: 0.5,
                    color: item.highlight ? 'error.main' : 'text.primary',
                    fontWeight: location.pathname === item.path ? 600 : 400,
                    position: 'relative',
                    '&::after': {
                      content: '""',
                      position: 'absolute',
                      bottom: 0,
                      left: 0,
                      width: '100%',
                      height: '3px',
                      bgcolor: item.highlight ? 'error.main' : 'primary.main',
                      opacity: location.pathname === item.path ? 1 : 0,
                      transition: 'opacity 0.3s',
                    },
                    '&:hover::after': {
                      opacity: 0.5,
                    },
                  }}
                >
                  {item.name}
                  {item.isNew && (
                    <Box
                      component="span"
                      sx={{
                        ml: 0.5,
                        fontSize: '0.6rem',
                        fontWeight: 'bold',
                        bgcolor: 'success.main',
                        color: 'white',
                        px: 0.5,
                        py: 0.1,
                        borderRadius: 1,
                        display: 'inline-flex',
                        alignItems: 'center',
                        position: 'absolute',
                        top: 0,
                        right: -5,
                      }}
                    >
                      NEW
                    </Box>
                  )}
                </Button>
              ))}
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {/* Top bar user actions */}
              <Box sx={{ ml: 'auto', display: 'flex', alignItems: 'center' }}>
                {/* Language selector */}
                <LanguageSelector />

                {/* Accessibility button */}
                <Tooltip title={t('Accessibility options')}>
                  <IconButton
                    color="inherit"
                    aria-label={t('Accessibility options')}
                    onClick={handleAccessibilityClick}
                  >
                    <AccessibilityNewIcon />
                  </IconButton>
                </Tooltip>

                {/* Notification Center (only show when authenticated) */}
                {isAuthenticated && <NotificationCenter />}

                {/* Login/Register or user profile buttons */}
                {isAuthenticated ? (
                  <Tooltip title={t('User menu')}>
                    <IconButton
                      edge="end"
                      color="inherit"
                      aria-label={t('User menu')}
                      onClick={handleUserMenuClick}
                    >
                      <Avatar
                        sx={{
                          width: 32,
                          height: 32,
                          bgcolor: theme.palette.primary.main,
                        }}
                      >
                        <AccountCircleIcon />
                      </Avatar>
                    </IconButton>
                  </Tooltip>
                ) : (
                  <Box sx={{ display: { xs: 'none', sm: 'flex' } }}>
                    <Button
                      component={Link}
                      to="/login"
                      color="inherit"
                      sx={{ ml: 1 }}
                      startIcon={<LoginIcon />}
                    >
                      {t('Login')}
                    </Button>
                    <Button
                      component={Link}
                      to="/register"
                      color="inherit"
                      sx={{ ml: 1 }}
                      startIcon={<PersonAddIcon />}
                    >
                      {t('Register')}
                    </Button>
                  </Box>
                )}
              </Box>

              {/* Legal Chat Button - Always accessible */}
              <Button
                component={Link}
                to="/legal-chat"
                color="inherit"
                startIcon={<ChatIcon />}
                sx={{
                  ml: { xs: 1, sm: 2 },
                  display: 'flex',
                  minWidth: { xs: 'auto', sm: 'auto' },
                  px: { xs: 1, sm: 2 }
                }}
              >
                {isMobile ? <ChatIcon /> : t('Legal Chat')}
              </Button>

              {/* Document Generator Button - Always accessible */}
              <Button
                component={Link}
                to="/documents"
                color="inherit"
                startIcon={<DescriptionIcon />}
                sx={{
                  ml: { xs: 1, sm: 2 },
                  display: 'flex',
                  minWidth: { xs: 'auto', sm: 'auto' },
                  px: { xs: 1, sm: 2 }
                }}
              >
                {isMobile ? <DescriptionIcon /> : t('Document Generator')}
              </Button>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      <SwipeableDrawer
        variant={isMobile ? 'temporary' : 'persistent'}
        open={mobileOpen}
        onOpen={handleDrawerToggle}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better mobile performance
        }}
        anchor="left"
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: { xs: '100%', sm: 280 },
            top: 0,
            height: '100%',
          },
        }}
      >
        {renderDrawer()}
      </SwipeableDrawer>

      {/* Enhanced User Menu */}
      <Menu
        id="user-menu"
        anchorEl={userMenuAnchor}
        open={Boolean(userMenuAnchor)}
        onClose={handleUserMenuClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        PaperProps={{
          sx: { 
            mt: 1.5,
            width: { xs: 220, sm: 280 },
            borderRadius: 1,
            boxShadow: 4,
          }
        }}
        MenuListProps={{
          sx: { py: 1 }
        }}
      >
        <Box sx={{ px: 2, py: 1.5 }}>
          <Typography variant="subtitle1" fontWeight={600} noWrap>
            {user?.name || user?.email || t('Your Account')}
          </Typography>
          <Typography variant="body2" color="text.secondary" noWrap>
            {user?.email}
          </Typography>
        </Box>
        <Divider />
        <MenuItem 
          onClick={() => {
            handleUserMenuClose();
            navigate('/profile');
          }}
          sx={{ py: 1.5, px: 2 }}
        >
          <ListItemIcon>
            <AccountCircleIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>{t('Profile')}</ListItemText>
        </MenuItem>
        <MenuItem 
          onClick={() => {
            handleUserMenuClose();
            navigate('/settings');
          }}
          sx={{ py: 1.5, px: 2 }}
        >
          <ListItemIcon>
            <SettingsIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>{t('Settings')}</ListItemText>
        </MenuItem>
        <Divider />
        <MenuItem 
          onClick={() => {
            handleUserMenuClose();
            handleLogout();
          }}
          sx={{ py: 1.5, px: 2 }}
        >
          <ListItemIcon>
            <ExitToAppIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>{t('Logout')}</ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
}

export default Navigation;
