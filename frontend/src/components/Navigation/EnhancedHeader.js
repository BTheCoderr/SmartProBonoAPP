import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Menu as MenuIcon,
  Home as HomeIcon,
  Scanner as ScannerIcon,
  Description as DocumentIcon,
  Chat as ChatIcon,
  Settings as SettingsIcon,
  Help as HelpIcon,
  AccountCircle as AccountIcon,
  Notifications as NotificationsIcon,
  Search as SearchIcon,
  MoreVert as MoreIcon,
  Legal as LegalIcon,
  Dashboard as DashboardIcon,
  ContactSupport as SupportIcon,
  Info as InfoIcon
} from '@mui/icons-material';

const EnhancedHeader = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleMobileMenuToggle = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const mainNavItems = [
    { label: 'Home', icon: <HomeIcon />, path: '/' },
    { label: 'Legal Tools', icon: <LegalIcon />, path: '/legal-tools' },
    { label: 'Document Scanner', icon: <ScannerIcon />, path: '/scan-document' },
    { label: 'PDF Generator', icon: <DocumentIcon />, path: '/generate-document' },
    { label: 'AI Legal Chat', icon: <ChatIcon />, path: '/legal-chat' }
  ];

  const toolsMenuItems = [
    { label: 'Document Scanner', icon: <ScannerIcon />, description: 'Analyze legal documents' },
    { label: 'PDF Generator', icon: <DocumentIcon />, description: 'Create legal documents' },
    { label: 'AI Legal Chat', icon: <ChatIcon />, description: 'Get legal advice' },
    { label: 'Templates', icon: <DocumentIcon />, description: 'Browse document templates' }
  ];

  const settingsMenuItems = [
    { label: 'Account Settings', icon: <AccountIcon /> },
    { label: 'Preferences', icon: <SettingsIcon /> },
    { label: 'Help & Support', icon: <HelpIcon /> },
    { label: 'About', icon: <InfoIcon /> }
  ];

  const renderDesktopNav = () => (
    <Toolbar>
      {/* Logo */}
      <Box sx={{ display: 'flex', alignItems: 'center', mr: 4 }}>
        <Box sx={{ 
          width: 40, 
          height: 40, 
          bgcolor: 'primary.main', 
          borderRadius: 1, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          mr: 1
        }}>
          <LegalIcon sx={{ color: 'white' }} />
        </Box>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
          SmartProBono
        </Typography>
        <Chip 
          label="BETA" 
          size="small" 
          color="success" 
          sx={{ ml: 1, height: 20, fontSize: '0.7rem' }}
        />
      </Box>

      {/* Main Navigation */}
      <Box sx={{ display: 'flex', gap: 1, mr: 'auto' }}>
        {mainNavItems.slice(0, 3).map((item) => (
          <Button
            key={item.label}
            color="inherit"
            startIcon={item.icon}
            sx={{ 
              textTransform: 'none',
              '&:hover': {
                bgcolor: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            {item.label}
          </Button>
        ))}
      </Box>

      {/* Tools Menu */}
      <Button
        color="inherit"
        onClick={handleMenuOpen}
        startIcon={<MoreIcon />}
        sx={{ textTransform: 'none', mr: 2 }}
      >
        More Tools
      </Button>

      {/* Right Side Actions */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <IconButton color="inherit">
          <SearchIcon />
        </IconButton>
        <IconButton color="inherit">
          <NotificationsIcon />
        </IconButton>
        <Button 
          color="inherit" 
          startIcon={<AccountIcon />}
          sx={{ textTransform: 'none' }}
        >
          Login
        </Button>
        <Button 
          variant="contained" 
          sx={{ 
            bgcolor: 'white', 
            color: 'primary.main',
            '&:hover': {
              bgcolor: 'grey.100'
            }
          }}
        >
          Sign Up
        </Button>
      </Box>
    </Toolbar>
  );

  const renderMobileNav = () => (
    <Toolbar>
      <IconButton
        color="inherit"
        aria-label="open drawer"
        edge="start"
        onClick={handleMobileMenuToggle}
        sx={{ mr: 2 }}
      >
        <MenuIcon />
      </IconButton>
      
      <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
        <Box sx={{ 
          width: 32, 
          height: 32, 
          bgcolor: 'white', 
          borderRadius: 1, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          mr: 1
        }}>
          <LegalIcon sx={{ color: 'primary.main', fontSize: 20 }} />
        </Box>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
          SmartProBono
        </Typography>
        <Chip 
          label="BETA" 
          size="small" 
          color="success" 
          sx={{ ml: 1, height: 18, fontSize: '0.6rem' }}
        />
      </Box>

      <Button 
        variant="contained" 
        size="small"
        sx={{ 
          bgcolor: 'white', 
          color: 'primary.main',
          '&:hover': {
            bgcolor: 'grey.100'
          }
        }}
      >
        Sign Up
      </Button>
    </Toolbar>
  );

  const renderToolsMenu = () => (
    <Menu
      anchorEl={anchorEl}
      open={Boolean(anchorEl)}
      onClose={handleMenuClose}
      PaperProps={{
        sx: { width: 300 }
      }}
    >
      <MenuItem disabled>
        <ListItemText>
          <Typography variant="subtitle2" color="text.secondary">
            Legal Tools
          </Typography>
        </ListItemText>
      </MenuItem>
      {toolsMenuItems.map((item) => (
        <MenuItem key={item.label} onClick={handleMenuClose}>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText 
            primary={item.label}
            secondary={item.description}
          />
        </MenuItem>
      ))}
      <Divider />
      <MenuItem disabled>
        <ListItemText>
          <Typography variant="subtitle2" color="text.secondary">
            Settings
          </Typography>
        </ListItemText>
      </MenuItem>
      {settingsMenuItems.map((item) => (
        <MenuItem key={item.label} onClick={handleMenuClose}>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.label} />
        </MenuItem>
      ))}
    </Menu>
  );

  const renderMobileDrawer = () => (
    <Drawer
      anchor="left"
      open={mobileMenuOpen}
      onClose={handleMobileMenuToggle}
    >
      <Box sx={{ width: 280, pt: 2 }}>
        <List>
          {mainNavItems.map((item) => (
            <ListItem key={item.label} disablePadding>
              <ListItemButton>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          ))}
          <Divider sx={{ my: 1 }} />
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon><SettingsIcon /></ListItemIcon>
              <ListItemText primary="Settings" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon><SupportIcon /></ListItemIcon>
              <ListItemText primary="Help & Support" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );

  return (
    <>
      <AppBar position="static" sx={{ bgcolor: 'primary.main' }}>
        {isMobile ? renderMobileNav() : renderDesktopNav()}
      </AppBar>
      
      {renderToolsMenu()}
      {renderMobileDrawer()}
    </>
  );
};

export default EnhancedHeader;
