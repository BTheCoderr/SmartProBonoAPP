import { createTheme, responsiveFontSizes } from '@mui/material/styles';

// Base font sizes for different settings
const fontSizes = {
  small: {
    h1: '2.25rem',
    h2: '1.875rem',
    h3: '1.5rem',
    h4: '1.25rem',
    h5: '1.125rem',
    h6: '1rem',
    body1: '0.875rem',
    body2: '0.8rem',
    button: '0.875rem',
    caption: '0.75rem',
  },
  medium: {
    h1: '2.75rem',
    h2: '2.25rem',
    h3: '1.875rem',
    h4: '1.625rem',
    h5: '1.375rem',
    h6: '1.125rem',
    body1: '1rem',
    body2: '0.875rem',
    button: '1rem',
    caption: '0.8125rem',
  },
  large: {
    h1: '3rem',
    h2: '2.5rem',
    h3: '2.125rem',
    h4: '1.75rem',
    h5: '1.5rem',
    h6: '1.25rem',
    body1: '1.125rem',
    body2: '1rem',
    button: '1.125rem',
    caption: '0.875rem',
  },
};

// Color palettes for different modes
const lightPalette = {
  primary: {
    main: '#2196F3',
    light: '#64B5F6',
    dark: '#1976D2',
    contrastText: '#FFFFFF',
  },
  secondary: {
    main: '#F50057',
    light: '#FF4081',
    dark: '#C51162',
    contrastText: '#FFFFFF',
  },
  background: {
    default: '#F5F5F5',
    paper: '#FFFFFF',
  },
  text: {
    primary: '#212121',
    secondary: '#757575',
    disabled: '#9E9E9E',
  },
};

const darkPalette = {
  primary: {
    main: '#90CAF9',
    light: '#BBDEFB',
    dark: '#42A5F5',
    contrastText: '#000000',
  },
  secondary: {
    main: '#FF80AB',
    light: '#FF99BC',
    dark: '#F06292',
    contrastText: '#000000',
  },
  background: {
    default: '#121212',
    paper: '#1E1E1E',
  },
  text: {
    primary: '#FFFFFF',
    secondary: '#B0B0B0',
    disabled: '#707070',
  },
};

const highContrastPalette = {
  primary: {
    main: '#FFFFFF',
    light: '#FFFFFF',
    dark: '#FFFFFF',
    contrastText: '#000000',
  },
  secondary: {
    main: '#FFFF00',
    light: '#FFFF33',
    dark: '#CCCC00',
    contrastText: '#000000',
  },
  background: {
    default: '#000000',
    paper: '#000000',
  },
  text: {
    primary: '#FFFFFF',
    secondary: '#FFFFFF',
    disabled: '#CCCCCC',
  },
  error: {
    main: '#FF6666',
    light: '#FF9999',
    dark: '#FF0000',
    contrastText: '#000000',
  },
  warning: {
    main: '#FFCC00',
    light: '#FFDD33',
    dark: '#CC9900',
    contrastText: '#000000',
  },
  info: {
    main: '#66CCFF',
    light: '#99DDFF',
    dark: '#0099FF',
    contrastText: '#000000',
  },
  success: {
    main: '#66FF66',
    light: '#99FF99',
    dark: '#00CC00',
    contrastText: '#000000',
  },
};

// Function to get theme options based on mode, contrast, and font size
const getThemeOptions = (mode = 'light', highContrast = false, fontSize = 'medium') => {
  // Determine which palette to use
  let palette;
  if (highContrast) {
    palette = highContrastPalette;
  } else if (mode === 'dark') {
    palette = darkPalette;
  } else {
    palette = lightPalette;
  }

  // Get font sizes based on setting
  const selectedFontSizes = fontSizes[fontSize] || fontSizes.medium;

  return {
    palette: {
      mode: highContrast ? 'dark' : mode,
      ...palette,
      error: palette.error || {
        main: mode === 'light' ? '#F44336' : '#FF6666',
      },
      warning: palette.warning || {
        main: mode === 'light' ? '#FF9800' : '#FFCC00',
      },
      info: palette.info || {
        main: mode === 'light' ? '#2196F3' : '#66CCFF',
      },
      success: palette.success || {
        main: mode === 'light' ? '#4CAF50' : '#66FF66',
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
        fontSize: selectedFontSizes.h1,
        fontWeight: 700,
        lineHeight: 1.2,
      },
      h2: {
        fontSize: selectedFontSizes.h2,
        fontWeight: 600,
        lineHeight: 1.3,
      },
      h3: {
        fontSize: selectedFontSizes.h3,
        fontWeight: 600,
        lineHeight: 1.3,
      },
      h4: {
        fontSize: selectedFontSizes.h4,
        fontWeight: 600,
        lineHeight: 1.4,
      },
      h5: {
        fontSize: selectedFontSizes.h5,
        fontWeight: 500,
        lineHeight: 1.4,
      },
      h6: {
        fontSize: selectedFontSizes.h6,
        fontWeight: 500,
        lineHeight: 1.5,
      },
      body1: {
        fontSize: selectedFontSizes.body1,
        lineHeight: 1.5,
      },
      body2: {
        fontSize: selectedFontSizes.body2,
        lineHeight: 1.5,
      },
      button: {
        fontSize: selectedFontSizes.button,
        textTransform: 'none',
        fontWeight: 500,
      },
      caption: {
        fontSize: selectedFontSizes.caption,
        lineHeight: 1.4,
      },
    },
    shape: {
      borderRadius: 8,
    },
    spacing: 8,
    breakpoints: {
      values: {
        xs: 0,
        sm: 600,
        md: 960,
        lg: 1280,
        xl: 1920,
      },
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: {
          // Improve mobile tap targets and text selection
          'html, body': {
            WebkitTapHighlightColor: 'transparent',
            WebkitTouchCallout: 'none',
            WebkitTextSizeAdjust: '100%',
          },
          // Fix 100vh issue on mobile browsers
          '#root': {
            minHeight: '100vh',
            minHeight: 'calc(var(--vh, 1vh) * 100)',
          },
          // Improve form element usability on mobile
          'input, select, textarea': {
            fontSize: '16px', // Prevents iOS zoom on focus
          },
        },
      },
      MuiButtonBase: {
        styleOverrides: {
          root: {
            // Disable the grey highlight on mobile tap
            '@media (hover: none)': {
              '&:hover': {
                backgroundColor: 'transparent',
              },
            },
          },
        },
        defaultProps: {
          // Reduce 300ms delay on mobile
          disableRipple: false,
          disableTouchRipple: false,
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 4,
            textTransform: 'none',
            padding: '10px 16px', // Increased vertical padding for touch targets
            // Minimum touch target size for mobile
            '@media (hover: none)': {
              minHeight: '44px',
              minWidth: '44px',
            },
            '&:focus': {
              outline: '3px solid yellow',
              outlineOffset: '2px',
            },
          },
          contained: {
            boxShadow: 'none',
            '&:hover': {
              boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.2)',
            },
          },
          sizeLarge: {
            padding: '12px 22px',
            fontSize: '1.0625rem',
          },
          sizeSmall: {
            padding: '6px 10px', 
            // Still maintain minimum touch target size on mobile
            '@media (hover: none)': {
              minHeight: '40px',
            },
          },
        },
        defaultProps: {
          disableElevation: true,
        },
      },
      MuiIconButton: {
        styleOverrides: {
          root: {
            // Increase tap target size on mobile
            '@media (hover: none)': {
              padding: '12px',
              minHeight: '48px',
              minWidth: '48px',
            },
          },
          sizeSmall: {
            // Still maintain proper touch target for small buttons on mobile
            '@media (hover: none)': {
              padding: '8px',
              minHeight: '40px',
              minWidth: '40px',
            },
          },
        },
      },
      MuiTextField: {
        styleOverrides: {
          root: {
            // Increase input field size on mobile for better touch targets
            '@media (hover: none)': {
              '& .MuiInputBase-root': {
                minHeight: '44px',
              },
            },
          },
        },
      },
      MuiInputBase: {
        styleOverrides: {
          input: {
            // Prevent autozoom on iOS
            '@media (hover: none)': {
              fontSize: '16px',
            },
          },
        },
      },
      MuiCardActionArea: {
        styleOverrides: {
          root: {
            // Better focus outline
            '&:focus-visible': {
              outline: `2px solid ${palette.primary.main}`,
              outlineOffset: '2px',
            },
          },
        },
      },
      MuiDialog: {
        styleOverrides: {
          paper: {
            // Better mobile dialogs
            '@media (max-width: 600px)': {
              margin: '16px',
              width: 'calc(100% - 32px)',
              maxHeight: 'calc(100% - 32px)',
              borderRadius: '8px',
            },
          },
        },
      },
      MuiDialogContent: {
        styleOverrides: {
          root: {
            // Adjust padding on mobile
            '@media (max-width: 600px)': {
              padding: '16px',
            },
          },
        },
      },
      MuiDialogActions: {
        styleOverrides: {
          root: {
            // Better spacing for action buttons on mobile
            '@media (max-width: 600px)': {
              padding: '8px 16px 16px',
            },
          },
        },
      },
      MuiListItem: {
        styleOverrides: {
          root: {
            // Better touch targets for list items on mobile
            '@media (hover: none)': {
              paddingTop: '12px',
              paddingBottom: '12px',
            },
          },
        },
      },
      MuiBottomNavigation: {
        styleOverrides: {
          root: {
            // Increased size for bottom navigation on mobile
            height: '64px',
          },
        },
      },
      MuiBottomNavigationAction: {
        styleOverrides: {
          root: {
            // Better labels on bottom navigation
            paddingTop: '8px',
            '&.Mui-selected': {
              paddingTop: '8px',
            },
          },
        },
      },
      MuiTableCell: {
        styleOverrides: {
          root: {
            // Better table rendering on mobile
            '@media (max-width: 600px)': {
              padding: '8px 12px',
              '&:first-of-type': {
                paddingLeft: '16px',
              },
              '&:last-of-type': {
                paddingRight: '16px',
              },
            },
          },
        },
      },
      MuiTab: {
        styleOverrides: {
          root: {
            // Proper tabs for mobile
            '@media (hover: none)': {
              minHeight: '48px',
            },
          },
        },
      },
      MuiSnackbar: {
        styleOverrides: {
          root: {
            // Better position for mobile snackbars
            '@media (max-width: 600px)': {
              left: '16px',
              right: '16px',
              bottom: '16px',
              width: 'auto',
            },
          },
        },
      },
      MuiSwitch: {
        styleOverrides: {
          root: {
            // Bigger touch target for switches
            '@media (hover: none)': {
              padding: '12px',
            },
          },
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            // Better sizing for mobile
            '@media (max-width: 600px)': {
              height: '28px',
              fontSize: '0.75rem',
            },
          },
        },
      },
      MuiPagination: {
        styleOverrides: {
          root: {
            // Better spacing for pagination on small screens
            '@media (max-width: 600px)': {
              '& .MuiPaginationItem-root': {
                minWidth: '32px',
                height: '32px',
              },
            },
          },
        },
      },
    },
  };
};

// Create the theme with a base configuration
const createAppTheme = (mode, highContrast, fontSize) => {
  let theme = createTheme(getThemeOptions(mode, highContrast, fontSize));
  
  // Add responsive font sizes
  theme = responsiveFontSizes(theme, {
    breakpoints: ['sm', 'md', 'lg'],
    factor: 0.5, // More conservative scaling factor for better mobile support
  });
  
  return theme;
};

// Default theme export
export default createAppTheme('light', false, 'medium');

// Export the theme creator function for use with theme provider
export { createAppTheme };
