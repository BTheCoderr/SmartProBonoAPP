import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';
import { motion } from 'framer-motion';
import { designTokens, layoutConstants } from '../DesignSystem';

const SectionContainer = styled(Box)(({ variant, background }) => {
  const backgroundStyles = {
    white: {
      backgroundColor: 'white',
    },
    light: {
      backgroundColor: designTokens.colors.neutral[50],
    },
    gradient: {
      background: designTokens.gradients.primary,
      color: 'white',
    },
    transparent: {
      backgroundColor: 'transparent',
    },
  };

  const variantStyles = {
    default: {
      padding: `${layoutConstants.sectionSpacing.md} 0`,
      borderRadius: { xs: 0, md: designTokens.borderRadius['2xl'] },
      margin: { xs: 0, md: designTokens.spacing[2] },
      boxShadow: { xs: 'none', md: '0 4px 20px rgba(0,0,0,0.08)' },
    },
    hero: {
      padding: `${layoutConstants.sectionSpacing.md} 0`,
      borderRadius: 0,
      margin: 0,
      boxShadow: 'none',
    },
    compact: {
      padding: `${layoutConstants.sectionSpacing.xs} 0`,
      borderRadius: { xs: 0, md: designTokens.borderRadius.lg },
      margin: { xs: 0, md: designTokens.spacing[2] },
      boxShadow: { xs: 'none', md: '0 2px 10px rgba(0,0,0,0.05)' },
    },
  };

  return {
    ...backgroundStyles[background || 'white'],
    ...variantStyles[variant || 'default'],
  };
});

const SectionHeader = styled(Box)({
  textAlign: 'center',
  marginBottom: { xs: designTokens.spacing[12], md: designTokens.spacing[16] },
});

const SectionBadge = styled(Chip)({
  marginBottom: designTokens.spacing[4],
  fontSize: '0.875rem',
  fontWeight: designTokens.typography.fontWeight.semibold,
  padding: `${designTokens.spacing[2]} ${designTokens.spacing[4]}`,
});

const SectionTitle = styled(Typography)({
  fontWeight: designTokens.typography.fontWeight.extrabold,
  fontSize: { xs: '2.5rem', md: '3rem' },
  lineHeight: designTokens.typography.lineHeight.snug,
  marginBottom: designTokens.spacing[4],
  color: designTokens.colors.neutral[800],
});

const SectionSubtitle = styled(Typography)({
  maxWidth: '700px',
  margin: '0 auto',
  lineHeight: designTokens.typography.lineHeight.relaxed,
  fontSize: { xs: '1.1rem', md: '1.25rem' },
  fontWeight: designTokens.typography.fontWeight.normal,
  color: designTokens.colors.neutral[500],
});

const Section = ({ 
  children,
  title,
  subtitle,
  badge,
  variant = 'default',
  background = 'white',
  header = true,
  ...props 
}) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94]
      }
    },
  };

  return (
    <SectionContainer variant={variant} background={background} {...props}>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
      >
        {header && (title || subtitle || badge) && (
          <motion.div variants={itemVariants}>
            <SectionHeader>
              {badge && (
                <SectionBadge
                  label={badge}
                  color="primary"
                />
              )}
              {title && (
                <SectionTitle variant="h2" gutterBottom>
                  {title}
                </SectionTitle>
              )}
              {subtitle && (
                <SectionSubtitle variant="h5">
                  {subtitle}
                </SectionSubtitle>
              )}
            </SectionHeader>
          </motion.div>
        )}
        
        <motion.div variants={itemVariants}>
          {children}
        </motion.div>
      </motion.div>
    </SectionContainer>
  );
};

export default Section;
