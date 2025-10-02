import React, { useState, useEffect } from 'react';
import { 
  AppBar, Toolbar, Typography, Button, IconButton, 
  Menu, MenuItem, Box, Avatar, Tooltip, 
  useMediaQuery, useTheme, Drawer, List, ListItem, 
  ListItemIcon, ListItemText, Chip, Container
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
import SearchIcon from '@mui/icons-material/Search';
import DescriptionIcon from '@mui/icons-material/Description';
import GavelIcon from '@mui/icons-material/Gavel';
import ChatIcon from '@mui/icons-material/Chat';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import ContactSupportIcon from '@mui/icons-material/ContactSupport';
import SecurityIcon from '@mui/icons-material/Security';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';
import Logo from './Logo';
import RealTimeNotification from './RealTimeNotification';

// HideOnScroll component removed - not currently used

const Header = () => {
  const { currentUser, logout, isBetaMode, enableBetaMode, disableBetaMode } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Mobile detection for responsive behavior
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [moreToolsAnchor, setMoreToolsAnchor] = useState(null);
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

  const handleMoreToolsMenu = (event) => {
    setMoreToolsAnchor(event.currentTarget);
  };

  const handleMoreToolsClose = () => {
    setMoreToolsAnchor(null);
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

  const mainMenuItems = [
    { text: t('navigation.home'), path: '/', icon: <HomeIcon />, badge: null },
    { text: t('navigation.legalTools'), path: '/legal-tools', icon: <GavelIcon />, badge: null },
    { text: t('navigation.documentScanner'), path: '/scan-document', icon: <DocumentScannerIcon />, badge: null },
    { text: t('navigation.pdfGenerator'), path: '/generate-document', icon: <DescriptionIcon />, badge: null },
    { text: t('navigation.aiLegalChat'), path: '/legal-chat', icon: <ChatIcon />, badge: null },
  ];

  const moreToolsItems = [
    { text: 'AI Virtual Paralegal', path: '/ai-virtual-paralegal', icon: <GavelIcon />, description: 'Autonomous AI legal assistant' },
    { text: 'Client Portal', path: '/client-portal', icon: <PersonIcon />, description: 'Client case management and tracking' },
    { text: 'Bondsman Dashboard', path: '/bondsman-dashboard', icon: <SecurityIcon />, description: 'Bail bond management system' },
    { text: t('navigation.templates'), path: '/templates', icon: <DescriptionIcon />, description: 'Browse document templates' },
    { text: t('navigation.safetyCheck'), path: '/safety-check', icon: <SecurityIcon />, description: 'Legal compliance checker' },
    { text: t('navigation.contactForm'), path: '/contact', icon: <ContactSupportIcon />, description: 'Get in touch with us' },
    { text: t('navigation.resources'), path: '/resources', icon: <MenuBookIcon />, description: 'Legal resources and guides' },
  ];

  const userMenuItems = [
    { text: t('navigation.dashboard'), path: '/dashboard', icon: <DashboardIcon />, authRequired: true },
    { text: t('navigation.forms'), path: '/forms', icon: <DocumentScannerIcon />, authRequired: true, badge: "New" },
    { text: t('navigation.chat'), path: '/chat', icon: <ForumIcon />, authRequired: true, badge: "AI" },
    { text: 'Client Portal', path: '/client-portal', icon: <PersonIcon />, authRequired: true, badge: "CRM" },
    { text: 'Bondsman Dashboard', path: '/bondsman-dashboard', icon: <SecurityIcon />, authRequired: true, badge: "CRM" },
    { text: 'AI Virtual Paralegal', path: '/ai-virtual-paralegal', icon: <GavelIcon />, authRequired: true, badge: "AI" },
  ];

  const profileMenuItems = [
    { text: t('navigation.profile'), path: '/profile', icon: <PersonIcon /> },
    ...(currentUser?.isAdmin ? [{ text: t('navigation.adminDashboard'), path: '/admin', icon: <AdminPanelSettingsIcon /> }] : []),
    { 
      text: isBetaMode ? t('navigation.disableBetaMode') : t('navigation.enableBetaMode'), 
      onClick: isBetaMode ? disableBetaMode : enableBetaMode, 
      icon: <Chip label={isBetaMode ? 'BETA ON' : 'BETA OFF'} size="small" color={isBetaMode ? 'success' : 'default'} />
    },
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
            {/* Main Menu Items */}
            {mainMenuItems.map((item) => (
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
            ))}

            {/* Divider */}
            <Box sx={{ my: 2, px: 2 }}>
              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                MORE TOOLS
              </Typography>
            </Box>

            {/* More Tools Items */}
            {moreToolsItems.map((item) => (
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
                  primary={item.text}
                  secondary={item.description}
                  secondaryTypographyProps={{ variant: 'caption' }}
                />
              </ListItem>
            ))}

            {/* User Menu Items (if logged in) */}
            {currentUser && (
              <>
                <Box sx={{ my: 2, px: 2 }}>
                  <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                    ACCOUNT
                  </Typography>
                </Box>
                {userMenuItems.map((item) => (
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
                ))}
              </>
            )}
          </List>

          {/* Language Switcher */}
          <Box sx={{ p: 2, borderTop: '1px solid rgba(0,0,0,0.1)' }} onClick={(e) => e.stopPropagation()}>
            <LanguageSwitcher />
          </Box>
        </Box>
      </Drawer>
    </>
  );

  return (
    <>
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
              {isBetaMode && (
                <Chip 
                  label="BETA" 
                  size="small" 
                  color="success" 
                  sx={{ 
                    ml: 1, 
                    fontSize: '0.7rem',
                    height: 20,
                    '& .MuiChip-label': {
                      px: 1
                    }
                  }} 
                />
              )}
            </Box>

            {/* Desktop Navigation */}
            {!isMobile && (
              <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
                {/* Main Menu Items */}
                {mainMenuItems.map((item) => (
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
                ))}

                {/* More Tools Dropdown */}
                <Button
                  onClick={handleMoreToolsMenu}
                  sx={{
                    color: scrolled ? 'rgba(0,0,0,0.8)' : 'rgba(0,0,0,0.7)',
                    mx: 1,
                    px: 2,
                    py: 1,
                    borderRadius: 2,
                    '&:hover': {
                      backgroundColor: 'rgba(59,130,246,0.1)',
                    },
                  }}
                  endIcon={<MoreVertIcon />}
                >
                  More Tools
                </Button>
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
                <Tooltip title="Real-time Notifications">
                  <RealTimeNotification />
                </Tooltip>
              )}

              {/* Language Switcher - Desktop */}
              {!isMobile && (
                <Box sx={{ ml: 1 }} onClick={(e) => e.stopPropagation()}>
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
                  {!isBetaMode && (
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={enableBetaMode}
                      sx={{
                        color: 'white',
                        borderColor: 'rgba(255,255,255,0.3)',
                        '&:hover': {
                          borderColor: 'white',
                          backgroundColor: 'rgba(255,255,255,0.1)',
                        },
                      }}
                    >
                      Beta Mode
                    </Button>
                  )}
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
                    {t('navigation.login')}
                  </Button>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={() => navigate('/register')}
                    sx={{
                      backgroundColor: 'white',
                      color: '#0F3D5E',
                      '&:hover': {
                        backgroundColor: 'rgba(255,255,255,0.9)',
                        color: '#0F3D5E',
                      },
                    }}
                  >
                    {t('navigation.register')}
                  </Button>
                </Box>
              )}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      {/* More Tools Menu */}
      <Menu
        anchorEl={moreToolsAnchor}
        open={Boolean(moreToolsAnchor)}
        onClose={handleMoreToolsClose}
        PaperProps={{
          sx: {
            mt: 1,
            minWidth: 280,
            borderRadius: 2,
            boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
          }
        }}
      >
        <MenuItem disabled>
          <ListItemText>
            <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 600 }}>
              {t('navigation.additionalTools')}
            </Typography>
          </ListItemText>
        </MenuItem>
        {moreToolsItems.map((item) => (
          <MenuItem
            key={item.text}
            onClick={() => {
              navigate(item.path);
              handleMoreToolsClose();
            }}
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
            <ListItemText 
              primary={item.text}
              secondary={item.description}
            />
          </MenuItem>
        ))}
      </Menu>
    </>
  );
};

export default Header; 