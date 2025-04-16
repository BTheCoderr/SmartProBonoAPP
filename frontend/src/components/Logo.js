import React from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import BalanceIcon from '@mui/icons-material/Balance';
import { styled } from '@mui/material/styles';
import PropTypes from 'prop-types';

const LogoText = styled(Typography)(({ theme, variant, size }) => {
  // Determine background gradient based on variant
  let background;
  let textFillColor = 'transparent';

  if (variant === 'light') {
    background = `linear-gradient(45deg, ${theme.palette.primary.dark} 30%, ${theme.palette.primary.main} 90%)`;
  } else if (variant === 'dark') {
    background = 'linear-gradient(45deg, #FFFFFF 30%, #E3F2FD 90%)';
  } else if (variant === 'highContrast') {
    background = 'none';
    textFillColor = '#FFFFFF';
  }

  return {
    background,
    WebkitBackgroundClip: variant === 'highContrast' ? 'unset' : 'text',
    WebkitTextFillColor: textFillColor,
    color: variant === 'highContrast' ? '#FFFFFF' : 'inherit',
    fontWeight: 700,
    display: 'inline',
    marginLeft: theme.spacing(1),
    fontSize: size === 'small' ? '1.25rem' : size === 'large' ? '2.5rem' : '1.5rem',
    letterSpacing: '0.5px',
    textShadow: variant === 'highContrast' ? '0px 0px 2px rgba(255,255,255,0.5)' : 'none',
  };
});

const Logo = ({ variant = 'light', size = 'medium' }) => {
  const theme = useTheme();

  const iconSizes = {
    small: '1.5rem',
    medium: '1.75rem',
    large: '2.5rem',
  };

  // Determine icon color based on variant
  let iconColor;
  if (variant === 'light') {
    iconColor = theme.palette.primary.main;
  } else if (variant === 'dark' || variant === 'highContrast') {
    iconColor = '#FFFFFF';
  }

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        '&:focus': {
          outline: variant === 'highContrast' ? '2px solid white' : 'none',
          outlineOffset: '4px',
        },
      }}
      role="img"
      aria-label="SmartProBono Logo"
    >
      <BalanceIcon
        sx={{
          fontSize: iconSizes[size],
          color: iconColor,
          filter:
            variant === 'highContrast' ? 'drop-shadow(0px 0px 2px rgba(255,255,255,0.5))' : 'none',
        }}
      />
      <LogoText variant={variant} size={size}>
        SmartProBono
      </LogoText>
    </Box>
  );
};

Logo.propTypes = {
  variant: PropTypes.oneOf(['light', 'dark', 'highContrast']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
};

export default Logo;
