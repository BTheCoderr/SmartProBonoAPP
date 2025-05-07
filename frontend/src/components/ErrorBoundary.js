import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    // Log error to analytics
    if (window.gtag) {
      window.gtag('event', 'error', {
        event_category: 'error_boundary',
        event_label: error.message,
        value: 1
      });
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            p: 3,
            textAlign: 'center'
          }}
        >
          <Typography variant="h4" gutterBottom>
            Something went wrong
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            We're sorry, but something went wrong. Our team has been notified and is working to fix the issue.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              this.setState({ hasError: false });
              window.location.reload();
            }}
            sx={{ mt: 2 }}
          >
            Try Again
          </Button>
          <Button
            variant="outlined"
            color="primary"
            onClick={() => window.location.href = '/'}
            sx={{ mt: 2, ml: 2 }}
          >
            Go to Home
          </Button>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary; 