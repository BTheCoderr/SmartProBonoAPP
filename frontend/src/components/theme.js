import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
  primary: {
      main: '#2196F3', // A professional blue color
    light: '#64B5F6',
    dark: '#1976D2',
  },
  secondary: {
      main: '#00796B', // Changed from pink to teal for more professional look
      light: '#B2DFDB',
      dark: '#004D40',
  },
  background: {
    default: '#F5F5F5',
    paper: '#FFFFFF',
      },
    },
    typography: {
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
      ].join(','),
      h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
      },
      h2: {
      fontSize: '2rem',
        fontWeight: 500,
      },
      body1: {
      fontSize: '1rem',
      },
    },
    shape: {
      borderRadius: 8,
    },
  spacing: 8, // Base spacing unit in px
}); 