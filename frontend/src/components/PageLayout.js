import React from 'react';
import { Box, Container, Typography, Paper, Breadcrumbs, Link } from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import PropTypes from 'prop-types';

const PageLayout = ({
  children,
  title,
  description,
  showBreadcrumbs = true,
  maxWidth = 'lg',
  sx = {},
}) => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter(x => x);

  // Map of path to display names
  const pathMap = {
    'legal-chat': 'Legal Chat',
    contracts: 'Contracts',
    rights: 'Rights',
    immigration: 'Immigration',
    services: 'Services',
    resources: 'Resources',
    contact: 'Contact',
  };

  return (
    <Box>
      {/* Page Header */}
      <Box
        sx={{
          background: 'linear-gradient(45deg, #1976d2 30%, #2196f3 90%)',
          color: 'white',
          pt: { xs: 4, md: 6 },
          pb: { xs: 4, md: 6 },
          position: 'relative',
          overflow: 'hidden',
          ...sx,
        }}
      >
        {/* Background Pattern */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            background: `
              linear-gradient(45deg, transparent 45%, #ffffff 45%, #ffffff 55%, transparent 55%),
              linear-gradient(-45deg, transparent 45%, #ffffff 45%, #ffffff 55%, transparent 55%)
            `,
            backgroundSize: '30px 30px',
          }}
        />

        <Container maxWidth={maxWidth} sx={{ position: 'relative' }}>
          {showBreadcrumbs && pathnames.length > 0 && (
            <Breadcrumbs
              separator={
                <NavigateNextIcon fontSize="small" sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
              }
              sx={{ mb: 2 }}
            >
              <Link
                component={RouterLink}
                to="/"
                sx={{
                  color: 'rgba(255, 255, 255, 0.7)',
                  textDecoration: 'none',
                  '&:hover': { color: 'white' },
                }}
              >
                Home
              </Link>
              {pathnames.map((name, index) => {
                const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
                const isLast = index === pathnames.length - 1;

                return isLast ? (
                  <Typography key={name} sx={{ color: 'white' }}>
                    {pathMap[name] || name}
                  </Typography>
                ) : (
                  <Link
                    key={name}
                    component={RouterLink}
                    to={routeTo}
                    sx={{
                      color: 'rgba(255, 255, 255, 0.7)',
                      textDecoration: 'none',
                      '&:hover': { color: 'white' },
                    }}
                  >
                    {pathMap[name] || name}
                  </Link>
                );
              })}
            </Breadcrumbs>
          )}

          <Typography
            variant="h3"
            gutterBottom
            sx={{
              fontWeight: 800,
              fontSize: { xs: '2rem', md: '2.5rem' },
              textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
            }}
          >
            {title}
          </Typography>
          {description && (
            <Typography
              variant="h6"
              sx={{
                maxWidth: '800px',
                opacity: 0.9,
                lineHeight: 1.5,
                fontWeight: 400,
              }}
            >
              {description}
            </Typography>
          )}
        </Container>
      </Box>

      {/* Page Content */}
      <Container
        maxWidth={maxWidth}
        sx={{
          py: { xs: 4, md: 6 },
          position: 'relative',
          zIndex: 1,
        }}
      >
        <Paper
          elevation={0}
          sx={{
            bgcolor: 'transparent',
          }}
        >
          {children}
        </Paper>
      </Container>
    </Box>
  );
};

PageLayout.propTypes = {
  /** Page content */
  children: PropTypes.node,
  /** Page title */
  title: PropTypes.string,
  /** Page description */
  description: PropTypes.string,
  /** Whether to show breadcrumbs */
  showBreadcrumbs: PropTypes.bool,
  /** Maximum width of the container */
  maxWidth: PropTypes.oneOf(['xs', 'sm', 'md', 'lg', 'xl']),
  /** Additional styles to apply to the box */
  sx: PropTypes.object
};

export default PageLayout;
