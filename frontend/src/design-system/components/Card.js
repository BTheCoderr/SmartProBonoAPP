import React from 'react';
import { Card as MuiCard, CardContent, CardActions } from '@mui/material';
import { styled } from '@mui/material/styles';
import { designTokens, componentVariants } from '../DesignSystem';

const StyledCard = styled(MuiCard, {
  shouldForwardProp: (prop) => prop !== 'hoverable',
})(({ variant, hoverable }) => {
  const baseStyles = {
    borderRadius: designTokens.borderRadius.lg,
    transition: `all ${designTokens.animations.duration.normal} ${designTokens.animations.easing.easeInOut}`,
    border: `1px solid ${designTokens.colors.neutral[200]}`,
  };

  // Variant styles
  const variantStyles = {
    default: {
      background: componentVariants.card.default.background,
      boxShadow: componentVariants.card.default.boxShadow,
      '&:hover': hoverable ? componentVariants.card.default.hover : {},
    },
    elevated: {
      background: componentVariants.card.elevated.background,
      boxShadow: componentVariants.card.elevated.boxShadow,
      border: componentVariants.card.elevated.border,
      '&:hover': hoverable ? componentVariants.card.elevated.hover : {},
    },
    gradient: {
      background: componentVariants.card.gradient.background,
      boxShadow: componentVariants.card.gradient.boxShadow,
      border: componentVariants.card.gradient.border,
    },
  };

  return {
    ...baseStyles,
    ...variantStyles[variant || 'default'],
  };
});

const StyledCardContent = styled(CardContent)({
  padding: designTokens.spacing[6],
  '&:last-child': {
    paddingBottom: designTokens.spacing[6],
  },
});

const StyledCardActions = styled(CardActions)({
  padding: `0 ${designTokens.spacing[6]} ${designTokens.spacing[6]}`,
  gap: designTokens.spacing[3],
});

const Card = ({ 
  children, 
  variant = 'default', 
  hoverable = true,
  content,
  actions,
  ...props 
}) => {
  return (
    <StyledCard variant={variant} hoverable={hoverable} {...props}>
      {content && <StyledCardContent>{content}</StyledCardContent>}
      {children}
      {actions && <StyledCardActions>{actions}</StyledCardActions>}
    </StyledCard>
  );
};

export default Card;
export { StyledCardContent as CardContent, StyledCardActions as CardActions };
