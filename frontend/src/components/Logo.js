import React from 'react';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

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

const Logo = ({ variant = 'light', size = 'medium', type = 'mark' }) => {
  const logoSizes = {
    small: { width: '32px', height: '32px' },
    medium: { width: '40px', height: '40px' },
    large: { width: '64px', height: '64px' }
  };

  // Choose logo source based on type
  const getLogoSrc = () => {
    switch (type) {
      case 'mark':
        return '/brand/smartprobono-mark.svg';
      case 'lockup':
        return '/brand/smartprobono-lockup.svg';
      case 'original':
        return '/smartprobonologo.png';
      default:
        return '/brand/smartprobono-mark.svg';
    }
  };

  return (
    <LogoContainer variant={variant}>
      <Box sx={{ 
        display: 'flex',
        alignItems: 'center',
        position: 'relative',
        filter: variant === 'light' ? 'drop-shadow(0px 2px 4px rgba(21, 101, 192, 0.5))' : 'none'
      }}>
        <img 
          src={getLogoSrc()} 
          alt="SmartProBono Logo"
          style={{
            ...logoSizes[size],
            objectFit: 'contain'
          }}
        />
        {type === 'text' && (
          <Typography 
            variant="h6" 
            sx={{ 
              ml: 1, 
              fontWeight: 'bold',
              color: variant === 'light' ? 'white' : 'primary.main'
            }}
          >
            SmartProBono
          </Typography>
        )}
      </Box>
    </LogoContainer>
  );
};

export default Logo; 