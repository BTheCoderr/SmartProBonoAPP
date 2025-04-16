import React from 'react';
import { Box, Alert, Button, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import PropTypes from 'prop-types';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      modelType: null,
    };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  componentDidCatch(error, errorInfo) {
    // Detect which model caused the error
    const modelType = this.detectModelType(error);
    this.setState({
      error,
      errorInfo,
      modelType,
    });
    // Log the error
    console.error('AI Model Error:', {
      model: modelType,
      error: error,
      info: errorInfo,
    });
  }
  detectModelType(error) {
    const errorMessage = error.message.toLowerCase();
    if (errorMessage.includes('tinyllama') || errorMessage.includes('chat')) {
      return 'chat';
    }
    if (errorMessage.includes('gpt2') || errorMessage.includes('document')) {
      return 'document';
    }
    if (errorMessage.includes('bloom') || errorMessage.includes('research')) {
      return 'research';
    }
    if (errorMessage.includes('falcon') || errorMessage.includes('analysis')) {
      return 'analysis';
    }
    return 'unknown';
  }
  getErrorMessage() {
    switch (this.state.modelType) {
      case 'chat':
        return {
          title: 'Chat Assistant Error',
          message: 'Our chat assistant is having trouble responding. Try rephrasing your question.',
          action: 'Try Again',
        };
      case 'document':
        return {
          title: 'Document Generation Error',
          message:
            'There was an issue generating your document. Please check your inputs and try again.',
          action: 'Retry Generation',
        };
      case 'research':
        return {
          title: 'Legal Research Error',
          message: 'We encountered an issue while researching. Try narrowing your search criteria.',
          action: 'Retry Research',
        };
      case 'analysis':
        return {
          title: 'Legal Analysis Error',
          message: 'Complex analysis failed. Try breaking down your request into smaller parts.',
          action: 'Retry Analysis',
        };
      default:
        return {
          title: 'Error',
          message: 'Something went wrong. Please try again.',
          action: 'Retry',
        };
    }
  }
  render() {
    if (this.state.hasError) {
      const errorInfo = this.getErrorMessage();
      return (
        <Box sx={{ p: 3 }}>
          <Alert
            severity="error"
            action={
              <Button
                color="inherit"
                size="small"
                startIcon={<RefreshIcon />}
                onClick={() => {
                  this.setState({ hasError: false });
                  window.location.reload();
                }}
              >
                {errorInfo.action}
              </Button>
            }
          >
            <Typography variant="h6" component="div" gutterBottom>
              {errorInfo.title}
            </Typography>
            <Typography variant="body2">{errorInfo.message}</Typography>
          </Alert>
        </Box>
      );
    }
    return this.props.children;
  }
}

// Define PropTypes
ErrorBoundary.propTypes = {
  /** React children to be rendered within the error boundary */
  children: PropTypes.node.isRequired
};

export default ErrorBoundary;