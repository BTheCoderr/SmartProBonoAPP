import React from 'react';
import {
  Card,
  CardContent,
  Box,
  Typography,
  Avatar,
  Rating,
  Chip,
  useTheme,
} from '@mui/material';
import { motion } from 'framer-motion';
import StarIcon from '@mui/icons-material/Star';
import VerifiedIcon from '@mui/icons-material/Verified';

const TestimonialCard = ({ testimonial, index }) => {
  const theme = useTheme();

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 50,
      scale: 0.95
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      transition: {
        duration: 0.6,
        delay: index * 0.1,
        ease: [0.25, 0.46, 0.45, 0.94]
      }
    },
    hover: {
      y: -8,
      scale: 1.02,
      transition: {
        duration: 0.3,
        ease: "easeOut"
      }
    }
  };

  const getRoleColor = (role) => {
    const roleColors = {
      'Immigration Client': 'primary',
      'Pro Bono Attorney': 'secondary',
      'Housing Rights Client': 'success',
      'Legal Aid Professional': 'info',
      'Small Claims Client': 'warning',
    };
    return roleColors[role] || 'default';
  };

  const getAvatarGradient = (name) => {
    const gradients = [
      'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    ];
    const index = name.charCodeAt(0) % gradients.length;
    return gradients[index];
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      style={{ height: '100%' }}
    >
      <Card
        sx={{
          height: '100%',
          background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
          border: `1px solid ${theme.palette.divider}`,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: getAvatarGradient(testimonial.name),
            opacity: 0.8,
          },
          '&:hover::before': {
            opacity: 1,
          },
        }}
      >
        <CardContent sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
          {/* Quote Icon */}
          <Box
            sx={{
              position: 'absolute',
              top: 16,
              right: 16,
              opacity: 0.1,
              fontSize: '3rem',
              color: theme.palette.primary.main,
              fontFamily: 'serif',
            }}
          >
            "
          </Box>

          {/* Header Section */}
          <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
            <Avatar
              sx={{
                width: 56,
                height: 56,
                mr: 2,
                background: getAvatarGradient(testimonial.name),
                fontSize: '1.5rem',
                fontWeight: 600,
                color: 'white',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              }}
            >
              {testimonial.avatar}
            </Avatar>
            
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: 700,
                    color: theme.palette.text.primary,
                    fontSize: '1.1rem',
                    lineHeight: 1.2,
                  }}
                >
                  {testimonial.name}
                </Typography>
                <VerifiedIcon
                  sx={{
                    ml: 1,
                    fontSize: '1rem',
                    color: theme.palette.success.main,
                  }}
                />
              </Box>
              
              <Chip
                label={testimonial.role}
                color={getRoleColor(testimonial.role)}
                size="small"
                sx={{
                  fontSize: '0.75rem',
                  height: 24,
                  fontWeight: 500,
                }}
              />
            </Box>
          </Box>

          {/* Rating */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Rating
              value={testimonial.rating}
              readOnly
              size="small"
              icon={<StarIcon sx={{ color: theme.palette.warning.main }} />}
              emptyIcon={<StarIcon sx={{ color: theme.palette.divider }} />}
              sx={{
                '& .MuiRating-iconFilled': {
                  color: theme.palette.warning.main,
                },
                '& .MuiRating-iconHover': {
                  color: theme.palette.warning.light,
                },
              }}
            />
            <Typography
              variant="caption"
              sx={{
                ml: 1,
                color: theme.palette.text.secondary,
                fontWeight: 500,
              }}
            >
              {testimonial.rating}.0 out of 5
            </Typography>
          </Box>

          {/* Testimonial Text */}
          <Typography
            variant="body1"
            sx={{
              flex: 1,
              color: theme.palette.text.primary,
              lineHeight: 1.6,
              fontSize: '0.95rem',
              fontStyle: 'italic',
              position: 'relative',
              '&::before': {
                content: '""',
                position: 'absolute',
                top: -8,
                left: -8,
                width: '2px',
                height: 'calc(100% + 16px)',
                background: getAvatarGradient(testimonial.name),
                borderRadius: '1px',
                opacity: 0.3,
              },
              pl: 2,
            }}
          >
            "{testimonial.text}"
          </Typography>

          {/* Footer */}
          <Box
            sx={{
              mt: 3,
              pt: 2,
              borderTop: `1px solid ${theme.palette.divider}`,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <Typography
              variant="caption"
              sx={{
                color: theme.palette.text.secondary,
                fontSize: '0.75rem',
                fontWeight: 500,
              }}
            >
              Verified User
            </Typography>
            
            <Box
              sx={{
                display: 'flex',
                gap: 0.5,
              }}
            >
              {[...Array(5)].map((_, i) => (
                <Box
                  key={i}
                  sx={{
                    width: 6,
                    height: 6,
                    borderRadius: '50%',
                    backgroundColor: i < testimonial.rating 
                      ? theme.palette.warning.main 
                      : theme.palette.divider,
                    opacity: 0.7,
                  }}
                />
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default TestimonialCard;
