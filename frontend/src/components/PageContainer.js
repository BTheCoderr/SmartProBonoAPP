import { Box } from '@mui/material';
import PropTypes from 'prop-types';

const PageContainer = ({ children }) => {
  return (
    <Box
      sx={{
        py: 4, // Padding top and bottom
        px: {
          xs: 2, // Padding left/right on mobile
          sm: 3, // Padding left/right on tablet
          md: 4, // Padding left/right on desktop
        },
        maxWidth: '1200px', // Maximum width
        mx: 'auto', // Center the container
        width: '100%',
        '& .MuiPaper-root': {
          // Consistent card spacing
          mb: 3,
        },
      }}
    >
      {children}
    </Box>
  );
};


// Define PropTypes
PageContainer.propTypes = {
  /** TODO: Add description */
  children: PropTypes.any,
};

export default PageContainer;
