import React from 'react';
import { Button as MuiButton } from '@mui/material';
import { styled } from '@mui/material/styles';
import { designTokens, componentVariants } from '../DesignSystem';

const StyledButton = styled(MuiButton)(({ variant, size, fullWidth }) => {
  const baseStyles = {
    fontFamily: designTokens.typography.fontFamily.primary,
    fontWeight: designTokens.typography.fontWeight.semibold,
    textTransform: 'none',
    borderRadius: designTokens.borderRadius.md,
    transition: `all ${designTokens.animations.duration.normal} ${designTokens.animations.easing.easeInOut}`,
    boxShadow: 'none',
    '&:hover': {
      boxShadow: designTokens.shadows.lg,
      transform: 'translateY(-2px)',
    },
    '&:active': {
      transform: 'translateY(0)',
    },
  };

  // Size variants
  const sizeStyles = {
    small: {
      padding: `${designTokens.spacing[2]} ${designTokens.spacing[4]}`,
      fontSize: designTokens.typography.fontSize.sm,
    },
    medium: {
      padding: `${designTokens.spacing[3]} ${designTokens.spacing[6]}`,
      fontSize: designTokens.typography.fontSize.base,
    },
    large: {
      padding: `${designTokens.spacing[4]} ${designTokens.spacing[8]}`,
      fontSize: designTokens.typography.fontSize.lg,
    },
  };

  // Variant styles
  const variantStyles = {
    primary: {
      background: componentVariants.button.primary.background,
      color: componentVariants.button.primary.color,
      '&:hover': {
        ...componentVariants.button.primary.hover,
        background: componentVariants.button.primary.background,
      },
    },
    secondary: {
      background: componentVariants.button.secondary.background,
      color: componentVariants.button.secondary.color,
      border: componentVariants.button.secondary.border,
      '&:hover': {
        ...componentVariants.button.secondary.hover,
        border: componentVariants.button.secondary.border,
      },
    },
    ghost: {
      background: componentVariants.button.ghost.background,
      color: componentVariants.button.ghost.color,
      '&:hover': {
        ...componentVariants.button.ghost.hover,
      },
    },
  };

  return {
    ...baseStyles,
    ...sizeStyles[size || 'medium'],
    ...variantStyles[variant || 'primary'],
    ...(fullWidth && { width: '100%' }),
  };
});

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  fullWidth = false,
  startIcon,
  endIcon,
  onClick,
  disabled = false,
  loading = false,
  ...props 
}) => {
  return (
    <StyledButton
      variant={variant}
      size={size}
      fullWidth={fullWidth}
      startIcon={startIcon}
      endIcon={endIcon}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? 'Loading...' : children}
    </StyledButton>
  );
};

export default Button;
