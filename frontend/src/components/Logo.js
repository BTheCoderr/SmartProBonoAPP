import React from 'react';
import { Box, Typography } from '@mui/material';
import BalanceIcon from '@mui/icons-material/Balance';
import GavelIcon from '@mui/icons-material/Gavel';
import { styled } from '@mui/material/styles';

const LogoText = styled(Typography)(({ theme, variant, size }) => ({
  background: variant === 'light' 
    ? 'linear-gradient(45deg, #1565C0 30%, #42A5F5 90%)'
    : 'linear-gradient(45deg, #FFFFFF 30%, #E3F2FD 90%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  fontWeight: 700,
  display: 'inline',
  marginLeft: theme.spacing(1),
  fontSize: size === 'small' ? '1.25rem' : size === 'large' ? '2.5rem' : '1.5rem',
  letterSpacing: '0.5px',
  textShadow: variant === 'light' ? '0px 0px 8px rgba(33, 150, 243, 0.3)' : 'none'
}));

const LogoContainer = styled(Box)(({ theme, variant }) => ({
  display: 'flex', 
  alignItems: 'center',
  padding: theme.spacing(0.5, 1),
  borderRadius: '4px',
  transition: 'transform 0.3s ease',
  '&:hover': {
    transform: 'scale(1.05)'
  }
}));

const Logo = ({ variant = 'light', size = 'medium' }) => {
  const iconSizes = {
    small: '1.5rem',
    medium: '1.75rem',
    large: '2.5rem'
  };

  return (
    <LogoContainer variant={variant}>
      <Box sx={{ 
        display: 'flex',
        alignItems: 'center',
        position: 'relative',
        filter: variant === 'light' ? 'drop-shadow(0px 2px 4px rgba(30, 136, 229, 0.5))' : 'none'
      }}>
        <BalanceIcon sx={{ 
          fontSize: iconSizes[size],
          color: variant === 'light' ? 'primary.main' : 'white',
          mr: -0.5,
          position: 'relative',
          zIndex: 2
        }} />
        <GavelIcon sx={{ 
          fontSize: iconSizes[size],
          color: variant === 'light' ? 'info.main' : 'white',
          position: 'relative',
          zIndex: 1,
          ml: -0.5
        }} />
      </Box>
      <LogoText variant={variant} size={size}>
        SmartProBono
      </LogoText>
    </LogoContainer>
  );
};

export default Logo; 