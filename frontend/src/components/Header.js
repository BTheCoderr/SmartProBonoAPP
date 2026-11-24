import React, { useState } from 'react';
import { AppBar, Box, Button, Drawer, IconButton, List, ListItemButton, ListItemText, Toolbar, Typography, useMediaQuery, useTheme } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import { Link as RouterLink, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import Logo from './Logo';

const Header = () => {
  const [open, setOpen] = useState(false);
  const { currentUser, logout } = useAuth();
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const theme = useTheme();
  const compact = useMediaQuery(theme.breakpoints.down('lg'));
  // Only links to routes mounted by App.js. Legacy prototypes remain in source.
  const links = [
    { path: '/', label: t('navigation.home', { defaultValue: 'Home' }) },
    { path: '/legal-chat', label: t('navigation.aiLegalChat', { defaultValue: 'AI Legal Chat' }) },
    { path: '/scan-document', label: t('navigation.documentScanner', { defaultValue: 'Document Scanner' }) },
    { path: '/about', label: 'About' },
    { path: '/contact', label: 'Contact' },
    ...(currentUser ? [{ path: '/dashboard', label: t('navigation.dashboard', { defaultValue: 'Dashboard' }) }] : []),
  ];
  const signOut = async () => {
    try {
      await logout();
      setOpen(false);
      navigate('/');
    } catch (error) {
      console.error('Logout failed', error);
    }
  };
  return (
    <>
      <AppBar position="sticky" elevation={1} sx={{ top: 0, bgcolor: '#fff', color: '#193851', borderRadius: 0, borderBottom: '1px solid #dce3eb' }}>
        <Toolbar disableGutters sx={{ width: '100%', maxWidth: 1440, mx: 'auto', px: { xs: 1.5, md: 3 }, minHeight: { xs: 64, md: 72 }, gap: 1, boxSizing: 'border-box' }}>
          {compact && <IconButton aria-label="Open navigation" aria-expanded={open} onClick={() => setOpen(true)} sx={{ color: '#193851', flexShrink: 0 }}><MenuIcon /></IconButton>}
          <Box component={RouterLink} to="/" aria-label="SmartProBono home" sx={{ display: 'flex', alignItems: 'center', flexShrink: 0, textDecoration: 'none', color: 'inherit' }}>
            <Logo size="medium" variant="dark" />
          </Box>
          {!compact && <Box component="nav" aria-label="Main navigation" sx={{ display: 'flex', alignItems: 'center', flex: 1, flexWrap: 'wrap', gap: 0.5 }}>
            {links.map(link => <Button key={link.path} component={RouterLink} to={link.path} aria-current={location.pathname === link.path ? 'page' : undefined} sx={{ color: '#193851', textTransform: 'none', fontWeight: location.pathname === link.path ? 700 : 500 }}>{link.label}</Button>)}
          </Box>}
          <Box sx={{ flex: compact ? 1 : 0 }} />
          {!compact && (currentUser ? <Button onClick={signOut} sx={{ color: '#193851' }}>Sign out</Button> : <Button component={RouterLink} to="/login" sx={{ color: '#193851' }}>Login</Button>)}
          <Button component="a" href="https://smartprobono.org" variant="contained" size="small" sx={{ bgcolor: '#193851', color: '#fff', whiteSpace: 'nowrap', textTransform: 'none', flexShrink: 0, '&:hover': { bgcolor: '#10263D' } }}>Current site</Button>
        </Toolbar>
      </AppBar>
      <Drawer open={open} onClose={() => setOpen(false)} PaperProps={{ sx: { width: 'min(300px, 90vw)' } }}>
        <Box component="nav" aria-label="Mobile navigation" sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="h6">SmartProBono</Typography>
            <IconButton aria-label="Close navigation" onClick={() => setOpen(false)}><CloseIcon /></IconButton>
          </Box>
          <Typography variant="body2" color="text.secondary">Legacy prototype</Typography>
          <List>
            {links.map(link => <ListItemButton key={link.path} component={RouterLink} to={link.path} selected={location.pathname === link.path} onClick={() => setOpen(false)}><ListItemText primary={link.label} /></ListItemButton>)}
            {currentUser ? <ListItemButton onClick={signOut}><ListItemText primary="Sign out" /></ListItemButton> : <>
              <ListItemButton component={RouterLink} to="/login" onClick={() => setOpen(false)}><ListItemText primary="Login" /></ListItemButton>
              <ListItemButton component={RouterLink} to="/register" onClick={() => setOpen(false)}><ListItemText primary="Register" /></ListItemButton>
            </>}
          </List>
        </Box>
      </Drawer>
    </>
  );
};

export default Header;
