import React from 'react';
import { Box, Container } from '@mui/material';
import { styled } from '@mui/material/styles';
import { designTokens, layoutConstants } from '../DesignSystem';

const StyledContainer = styled(Container)(({ maxWidth = 'lg' }) => ({
  maxWidth: layoutConstants.maxWidth[maxWidth] || maxWidth,
  paddingLeft: layoutConstants.containerPadding.lg,
  paddingRight: layoutConstants.containerPadding.lg,
  '@media (max-width: 900px)': {
    paddingLeft: layoutConstants.containerPadding.md,
    paddingRight: layoutConstants.containerPadding.md,
  },
  '@media (max-width: 600px)': {
    paddingLeft: layoutConstants.containerPadding.sm,
    paddingRight: layoutConstants.containerPadding.sm,
  },
}));

const PageLayout = ({ 
  children, 
  maxWidth = 'lg',
  background = 'default',
  padding = 'normal',
  ...props 
}) => {
  const backgroundStyles = {
    default: {
      backgroundColor: designTokens.colors.neutral[50],
    },
    white: {
      backgroundColor: 'white',
    },
    gradient: {
      background: designTokens.gradients.primary,
    },
    transparent: {
      backgroundColor: 'transparent',
    },
  };

  const paddingStyles = {
    none: { padding: 0 },
    small: { padding: designTokens.spacing[8] },
    normal: { padding: designTokens.spacing[12] },
    large: { padding: designTokens.spacing[16] },
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        ...backgroundStyles[background],
        ...paddingStyles[padding],
        ...props.sx,
      }}
      {...props}
    >
      <StyledContainer maxWidth={maxWidth}>
        {children}
      </StyledContainer>
    </Box>
  );
};

export default PageLayout;
