import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import RefreshIcon from '@mui/icons-material/Refresh';

class FeatureErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // Log error to your error reporting service
    console.error('Feature Error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    if (this.props.onRetry) {
      this.props.onRetry();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <Paper
          elevation={3}
          sx={{
            p: 3,
            m: 2,
            textAlign: 'center',
            backgroundColor: 'background.paper',
            borderRadius: 2
          }}
        >
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2
            }}
          >
            <ErrorOutlineIcon
              color="error"
              sx={{ fontSize: 64 }}
              aria-hidden="true"
            />
            <Typography variant="h5" component="h2" gutterBottom>
              {this.props.featureName || 'Feature'} Error
            </Typography>
            <Typography variant="body1" color="text.secondary" gutterBottom>
              {this.props.errorMessage || 'Something went wrong with this feature.'}
            </Typography>
            {process.env.NODE_ENV === 'development' && (
              <Box
                sx={{
                  mt: 2,
                  p: 2,
                  backgroundColor: 'grey.100',
                  borderRadius: 1,
                  textAlign: 'left',
                  maxWidth: '100%',
                  overflow: 'auto'
                }}
              >
                <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                  {this.state.error?.toString()}
                </Typography>
              </Box>
            )}
            <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={this.handleRetry}
                startIcon={<RefreshIcon />}
                aria-label="Retry feature"
              >
                Try Again
              </Button>
              {this.props.onContactSupport && (
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={this.props.onContactSupport}
                  aria-label="Contact support"
                >
                  Contact Support
                </Button>
              )}
            </Box>
          </Box>
        </Paper>
      );
    }

    return this.props.children;
  }
}

export default FeatureErrorBoundary; 