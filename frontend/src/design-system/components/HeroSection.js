import React from 'react';
import { Box, Typography, Stack, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';
import { motion } from 'framer-motion';
import { designTokens } from '../DesignSystem';
import Button from './Button';

const HeroContainer = styled(Box)({
  background: designTokens.gradients.hero,
  color: 'white',
  position: 'relative',
  overflow: 'hidden',
  borderRadius: { xs: 0, md: '0 0 40px 40px' },
  margin: { xs: 0, md: designTokens.spacing[2] },
  marginBottom: { xs: 0, md: designTokens.spacing[4] },
  boxShadow: '0 8px 32px rgba(30, 64, 175, 0.3)',
  paddingTop: { xs: designTokens.spacing[12], md: designTokens.spacing[16] },
  paddingBottom: { xs: designTokens.spacing[12], md: designTokens.spacing[16] },
});

const Overlay = styled(Box)({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  background: 'rgba(0, 0, 0, 0.4)',
  zIndex: 1,
});

const BackgroundPattern = styled(Box)({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  opacity: 0.1,
  background: `
    radial-gradient(circle at 20% 80%, rgba(255,255,255,0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(255,255,255,0.2) 0%, transparent 50%)
  `,
});

const ContentContainer = styled(Box)({
  position: 'relative',
  zIndex: 3,
});

const HeroTitle = styled(Typography)({
  fontWeight: designTokens.typography.fontWeight.black,
  fontSize: { xs: '2.5rem', sm: '3rem', md: '3.5rem' },
  lineHeight: designTokens.typography.lineHeight.tight,
  textShadow: '0 4px 12px rgba(0,0,0,0.5)',
  marginBottom: designTokens.spacing[6],
  color: '#ffffff',
});

const HeroSubtitle = styled(Typography)({
  marginBottom: designTokens.spacing[8],
  opacity: 1,
  maxWidth: '600px',
  lineHeight: designTokens.typography.lineHeight.relaxed,
  fontSize: { xs: '1.1rem', md: '1.25rem' },
  fontWeight: designTokens.typography.fontWeight.medium,
  color: '#ffffff',
  textShadow: '0 2px 8px rgba(0,0,0,0.4)',
});

const StatsContainer = styled(Box)({
  display: 'flex',
  gap: designTokens.spacing[6],
  marginBottom: designTokens.spacing[8],
  flexWrap: 'wrap',
});

const StatItem = styled(Box)({
  textAlign: 'center',
});

const StatValue = styled(Typography)({
  fontWeight: designTokens.typography.fontWeight.extrabold,
  fontSize: '1.5rem',
  marginBottom: designTokens.spacing[1],
  color: '#ffffff',
  textShadow: '0 2px 6px rgba(0,0,0,0.4)',
});

const StatLabel = styled(Typography)({
  opacity: 1,
  fontSize: '0.75rem',
  fontWeight: designTokens.typography.fontWeight.semibold,
  color: '#ffffff',
  textShadow: '0 1px 4px rgba(0,0,0,0.4)',
});

const TrustSignalsContainer = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: designTokens.spacing[6],
  flexWrap: 'wrap',
});

const TrustSignal = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: designTokens.spacing[2],
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  padding: `${designTokens.spacing[2]} ${designTokens.spacing[4]}`,
  borderRadius: designTokens.borderRadius.lg,
  backdropFilter: 'blur(10px)',
});

const TrustSignalText = styled(Typography)({
  fontWeight: designTokens.typography.fontWeight.semibold,
  fontSize: '0.75rem',
  color: '#ffffff',
  textShadow: '0 1px 4px rgba(0,0,0,0.4)',
});

const HeroSection = ({ 
  title,
  subtitle,
  badge,
  stats = [],
  trustSignals = [],
  actions = [],
  children 
}) => {
  const heroVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.2,
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
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  const floatingAnimation = {
    y: [0, -10, 0],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: "easeInOut",
    },
  };

  return (
    <HeroContainer
      component={motion.div}
      variants={heroVariants}
      initial="hidden"
      animate="visible"
    >
      <Overlay />
      <BackgroundPattern />
      
      {/* Floating Shapes */}
      <motion.div
        animate={floatingAnimation}
        style={{
          position: 'absolute',
          top: '20%',
          right: '10%',
          width: 60,
          height: 60,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
        }}
      />
      <motion.div
        animate={{ ...floatingAnimation, delay: 1 }}
        style={{
          position: 'absolute',
          top: '60%',
          left: '5%',
          width: 40,
          height: 40,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
        }}
      />

      <ContentContainer>
        <motion.div variants={itemVariants}>
          {/* Badge */}
          {badge && (
            <Chip
              label={badge}
              color="secondary"
              sx={{
                marginBottom: designTokens.spacing[6],
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                fontWeight: designTokens.typography.fontWeight.semibold,
                fontSize: '0.875rem',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.3)',
                },
              }}
            />
          )}

          {/* Title */}
          {title && (
            <HeroTitle variant="h1" gutterBottom>
              {title}
            </HeroTitle>
          )}

          {/* Subtitle */}
          {subtitle && (
            <HeroSubtitle variant="h5" paragraph>
              {subtitle}
            </HeroSubtitle>
          )}

          {/* Stats */}
          {stats.length > 0 && (
            <StatsContainer>
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                  transition={{ delay: 0.5 + index * 0.1 }}
                >
                  <StatItem>
                    <StatValue variant="h4">
                      {stat.value}
                    </StatValue>
                    <StatLabel variant="caption">
                      {stat.label}
                    </StatLabel>
                  </StatItem>
                </motion.div>
              ))}
            </StatsContainer>
          )}

          {/* Actions */}
          {actions.length > 0 && (
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={designTokens.spacing[4]}
              sx={{ marginBottom: designTokens.spacing[8] }}
            >
              {actions.map((action, index) => (
                <motion.div
                  key={index}
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                  transition={{ delay: 0.3 + index * 0.1 }}
                >
                  <Button
                    variant={action.variant || 'primary'}
                    size="large"
                    startIcon={action.icon}
                    onClick={action.onClick}
                    sx={action.sx}
                  >
                    {action.label}
                  </Button>
                </motion.div>
              ))}
            </Stack>
          )}

          {/* Trust Signals */}
          {trustSignals.length > 0 && (
            <TrustSignalsContainer>
              <Typography
                variant="body2"
                sx={{
                  opacity: 1,
                  fontWeight: designTokens.typography.fontWeight.semibold,
                  color: '#ffffff',
                  textShadow: '0 1px 4px rgba(0,0,0,0.4)',
                }}
              >
                Trusted by:
              </Typography>
              {trustSignals.map((signal, index) => (
                <motion.div
                  key={signal.text}
                  variants={itemVariants}
                  initial="hidden"
                  animate="visible"
                  transition={{ delay: 0.8 + index * 0.1 }}
                >
                  <TrustSignal>
                    {signal.icon}
                    <TrustSignalText variant="caption">
                      {signal.text}
                    </TrustSignalText>
                  </TrustSignal>
                </motion.div>
              ))}
            </TrustSignalsContainer>
          )}

          {children}
        </motion.div>
      </ContentContainer>
    </HeroContainer>
  );
};

export default HeroSection;
