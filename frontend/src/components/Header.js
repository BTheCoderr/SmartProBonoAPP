import React, { useState, useEffect } from 'react';
import { 
  AppBar, Toolbar, Typography, Button, IconButton, 
  Menu, MenuItem, Box, Avatar, Tooltip, 
  useMediaQuery, useTheme, Drawer, List, ListItem, 
  ListItemIcon, ListItemText, Badge, Chip, useScrollTrigger,
  Slide, Container
} from '@mui/material';
import { Link as RouterLink, useNavigate, useLocation } from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ForumIcon from '@mui/icons-material/Forum';
import PersonIcon from '@mui/icons-material/Person';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import LogoutIcon from '@mui/icons-material/Logout';
import DocumentScannerIcon from '@mui/icons-material/DocumentScanner';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SearchIcon from '@mui/icons-material/Search';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';
import Logo from './Logo';

// Hide header on scroll down, show on scroll up
function HideOnScroll(props) {
  const { children } = props;
  const trigger = useScrollTrigger();

  return (
    <Slide appear={false} direction="down" in={!trigger}>
      {children}
    </Slide>
  );
}

const Header = () => {
  const { currentUser, logout } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  
  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 20;
      setScrolled(isScrolled);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Logout failed', error);
    }
    handleClose();
  };

  const toggleDrawer = (open) => (event) => {
    if (
      event.type === 'keydown' &&
      (event.key === 'Tab' || event.key === 'Shift')
    ) {
      return;
    }
    setDrawerOpen(open);
  };

  const menuItems = [
    { text: t('navigation.home'), path: '/', icon: <HomeIcon />, badge: null },
    { text: t('navigation.dashboard'), path: '/dashboard', icon: <DashboardIcon />, authRequired: true, badge: null },
    { text: t('navigation.forms'), path: '/forms', icon: <DocumentScannerIcon />, authRequired: true, badge: "New" },
    { text: t('navigation.chat'), path: '/chat', icon: <ForumIcon />, authRequired: true, badge: "AI" },
    { text: t('navigation.resources'), path: '/resources', icon: <MenuBookIcon />, badge: null },
    { text: 'Document Analysis', path: '/document-scan', icon: <DocumentScannerIcon />, authRequired: true, badge: "AI" },
  ];

  const profileMenuItems = [
    { text: t('navigation.profile'), path: '/profile', icon: <PersonIcon /> },
    ...(currentUser?.isAdmin ? [{ text: 'Admin Dashboard', path: '/admin', icon: <AdminPanelSettingsIcon /> }] : []),
    { text: t('navigation.logout'), onClick: handleLogout, icon: <LogoutIcon /> },
  ];

  const isActivePath = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  const renderMobileDrawer = () => (
    <>
      <IconButton
        edge="start"
        color="inherit"
        aria-label="menu"
        onClick={toggleDrawer(true)}
        sx={{
          display: { md: 'none' },
          color: scrolled ? 'rgba(0,0,0,0.8)' : 'rgba(0,0,0,0.7)',
        }}
      >
        <MenuIcon />
      </IconButton>
      <Drawer 
        anchor="left" 
        open={drawerOpen} 
        onClose={toggleDrawer(false)}
        PaperProps={{
          sx: {
            width: 280,
            background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
            color: 'rgba(0,0,0,0.8)',
          }
        }}
      >
        <Box
          sx={{ 
            width: 280,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
          }}
          role="presentation"
          onClick={toggleDrawer(false)}
          onKeyDown={toggleDrawer(false)}
        >
          {/* Drawer Header */}
          <Box sx={{ p: 3, borderBottom: '1px solid rgba(0,0,0,0.1)' }}>
            <Logo />
            <Typography variant="body2" sx={{ mt: 1, opacity: 0.7, color: 'rgba(0,0,0,0.7)' }}>
              Legal Help Made Simple
            </Typography>
          </Box>

          {/* User Info */}
          {currentUser && (
            <Box sx={{ p: 3, borderBottom: '1px solid rgba(0,0,0,0.1)' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar
                  sx={{
                    bgcolor: theme.palette.primary.main,
                    mr: 2,
                    width: 40,
                    height: 40,
                  }}
                >
                  {currentUser.first_name?.[0]}{currentUser.last_name?.[0]}
                </Avatar>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'rgba(0,0,0,0.9)' }}>
                    {currentUser.first_name} {currentUser.last_name}
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.7, color: 'rgba(0,0,0,0.6)' }}>
                    {currentUser.email}
                  </Typography>
                </Box>
              </Box>
            </Box>
          )}

          {/* Navigation Items */}
          <List sx={{ flex: 1, px: 2 }}>
            {menuItems.map((item) => (
              (!item.authRequired || currentUser) && (
                <ListItem 
                  button 
                  component={RouterLink} 
                  to={item.path} 
                  key={item.text}
                  sx={{
                    mb: 1,
                    borderRadius: 2,
                    backgroundColor: isActivePath(item.path) ? 'rgba(59,130,246,0.1)' : 'transparent',
                    '&:hover': {
                      backgroundColor: 'rgba(59,130,246,0.1)',
                    },
                  }}
                >
                  <ListItemIcon sx={{ color: 'rgba(0,0,0,0.7)', minWidth: 40 }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText 
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {item.text}
                        {item.badge && (
                          <Chip
                            label={item.badge}
                            size="small"
                            color="primary"
                            sx={{
                              height: 20,
                              fontSize: '0.7rem',
                              fontWeight: 600,
                            }}
                          />
                        )}
                      </Box>
                    }
                  />
                </ListItem>
              )
            ))}
          </List>

          {/* Language Switcher */}
          <Box sx={{ p: 2, borderTop: '1px solid rgba(0,0,0,0.1)' }}>
            <LanguageSwitcher />
          </Box>
        </Box>
      </Drawer>
    </>
  );

  return (
    <HideOnScroll>
      <AppBar
        position="fixed"
        sx={{
          background: scrolled 
            ? 'rgba(255, 255, 255, 0.95)' 
            : 'rgba(255, 255, 255, 0.1)',
          backdropFilter: scrolled ? 'blur(20px)' : 'blur(10px)',
          boxShadow: scrolled ? '0 4px 20px rgba(0,0,0,0.1)' : '0 2px 10px rgba(0,0,0,0.05)',
          transition: 'all 0.3s ease',
          borderBottom: scrolled ? '1px solid rgba(0,0,0,0.1)' : '1px solid rgba(255,255,255,0.2)',
        }}
      >
        <Container maxWidth="xl">
          <Toolbar sx={{ px: { xs: 1, sm: 2 }, py: 1 }}>
            {/* Mobile Menu Button */}
            {renderMobileDrawer()}

            {/* Logo */}
            <Box sx={{ display: 'flex', alignItems: 'center', mr: { xs: 1, sm: 3 } }}>
              <Logo />
              {!isSmallMobile && (
                <Typography
                  variant="h6"
                  sx={{
                    ml: 1,
                    fontWeight: 700,
                    background: 'linear-gradient(45deg, #1e40af 30%, #3b82f6 90%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    display: { xs: 'none', sm: 'block' },
                  }}
                >
                  SmartProBono
                </Typography>
              )}
            </Box>

            {/* Desktop Navigation */}
            {!isMobile && (
              <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
                {menuItems.map((item) => (
                  (!item.authRequired || currentUser) && (
                    <Button
                      key={item.text}
                      component={RouterLink}
                      to={item.path}
                      sx={{
                        color: scrolled ? 'rgba(0,0,0,0.8)' : 'rgba(0,0,0,0.7)',
                        mx: 1,
                        px: 2,
                        py: 1,
                        borderRadius: 2,
                        position: 'relative',
                        backgroundColor: isActivePath(item.path) ? 'rgba(59,130,246,0.1)' : 'transparent',
                        '&:hover': {
                          backgroundColor: 'rgba(59,130,246,0.1)',
                        },
                        '&::after': {
                          content: '""',
                          position: 'absolute',
                          bottom: 0,
                          left: '50%',
                          transform: 'translateX(-50%)',
                          width: isActivePath(item.path) ? '20px' : '0px',
                          height: '2px',
                          backgroundColor: theme.palette.primary.light,
                          transition: 'width 0.3s ease',
                        },
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {item.icon}
                        {item.text}
                        {item.badge && (
                          <Chip
                            label={item.badge}
                            size="small"
                            color="primary"
                            sx={{
                              height: 20,
                              fontSize: '0.7rem',
                              fontWeight: 600,
                              ml: 0.5,
                            }}
                          />
                        )}
                      </Box>
                    </Button>
                  )
                ))}
              </Box>
            )}

            {/* Right Side Actions */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              {/* Search Button */}
              <Tooltip title="Search">
                <IconButton
                  sx={{ color: 'white' }}
                  onClick={() => navigate('/search')}
                >
                  <SearchIcon />
                </IconButton>
              </Tooltip>

              {/* Notifications */}
              {currentUser && (
                <Tooltip title="Notifications">
                  <IconButton
                    sx={{ color: 'white' }}
                    onClick={() => navigate('/notifications')}
                  >
                    <Badge badgeContent={3} color="error">
                      <NotificationsIcon />
                    </Badge>
                  </IconButton>
                </Tooltip>
              )}

              {/* Language Switcher - Desktop */}
              {!isMobile && (
                <Box sx={{ ml: 1 }}>
                  <LanguageSwitcher />
                </Box>
              )}

              {/* User Menu */}
              {currentUser ? (
                <>
                  <Tooltip title="Account settings">
                    <IconButton
                      onClick={handleMenu}
                      sx={{
                        color: 'white',
                        ml: 1,
                        border: '2px solid rgba(255,255,255,0.2)',
                        '&:hover': {
                          borderColor: 'rgba(255,255,255,0.4)',
                        },
                      }}
                    >
                      <Avatar
                        sx={{
                          bgcolor: theme.palette.primary.main,
                          width: 32,
                          height: 32,
                          fontSize: '0.875rem',
                        }}
                      >
                        {currentUser.first_name?.[0]}{currentUser.last_name?.[0]}
                      </Avatar>
                    </IconButton>
                  </Tooltip>
                  <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                    PaperProps={{
                      sx: {
                        mt: 1,
                        minWidth: 200,
                        borderRadius: 2,
                        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
                      }
                    }}
                  >
                    {profileMenuItems.map((item) => (
                      <MenuItem
                        key={item.text}
                        onClick={item.onClick || (() => navigate(item.path))}
                        sx={{
                          py: 1.5,
                          px: 2,
                          '&:hover': {
                            backgroundColor: theme.palette.action.hover,
                          },
                        }}
                      >
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          {item.icon}
                        </ListItemIcon>
                        <ListItemText primary={item.text} />
                      </MenuItem>
                    ))}
                  </Menu>
                </>
              ) : (
                <Box sx={{ display: 'flex', gap: 1, ml: 2 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => navigate('/login')}
                    sx={{
                      color: 'white',
                      borderColor: 'rgba(255,255,255,0.3)',
                      '&:hover': {
                        borderColor: 'white',
                        backgroundColor: 'rgba(255,255,255,0.1)',
                      },
                    }}
                  >
                    Login
                  </Button>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={() => navigate('/register')}
                    sx={{
                      backgroundColor: 'white',
                      color: theme.palette.primary.main,
                      '&:hover': {
                        backgroundColor: 'rgba(255,255,255,0.9)',
                      },
                    }}
                  >
                    Sign Up
                  </Button>
                </Box>
              )}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
    </HideOnScroll>
  );
};

export default Header; 