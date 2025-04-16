import React, { createContext, useState, useContext, useEffect } from 'react';
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { getThemeOptions } from '../components/theme';

// Create the context
export const ThemeContext = createContext();

// Custom hook to use the theme context
export const useThemeContext = () => useContext(ThemeContext);

// Theme provider component
export const ThemeProvider = ({ children }) => {
  // State for theme settings
  const [mode, setMode] = useState(() => {
    const savedMode = localStorage.getItem('themeMode');
    return savedMode || 'light';
  });

  const [highContrast, setHighContrast] = useState(() => {
    const savedContrast = localStorage.getItem('highContrast');
    return savedContrast === 'true';
  });

  const [fontSize, setFontSize] = useState(() => {
    const savedSize = localStorage.getItem('fontSize');
    return savedSize || 'medium';
  });

  // Create theme based on current settings
  const theme = React.useMemo(() => {
    const themeOptions = getThemeOptions(mode, highContrast, fontSize);
    return createTheme(themeOptions);
  }, [mode, highContrast, fontSize]);

  // Save theme preferences to localStorage
  useEffect(() => {
    localStorage.setItem('themeMode', mode);
    localStorage.setItem('highContrast', highContrast.toString());
    localStorage.setItem('fontSize', fontSize);
  }, [mode, highContrast, fontSize]);

  // Context value
  const contextValue = {
    mode,
    setMode,
    highContrast,
    setHighContrast,
    fontSize,
    setFontSize,
    // Helper functions
    toggleMode: () => setMode(prevMode => (prevMode === 'light' ? 'dark' : 'light')),
    toggleHighContrast: () => setHighContrast(prev => !prev),
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
