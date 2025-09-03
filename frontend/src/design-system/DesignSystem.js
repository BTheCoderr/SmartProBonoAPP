/**
 * SmartProBono Design System
 * Single source of truth for all design tokens and components
 */

// Design Tokens
export const designTokens = {
  colors: {
    // Primary Palette - SmartProBono Navy
    primary: {
      50: '#f0f4f8',
      100: '#d9e2ec', 
      200: '#bcccdc',
      300: '#9fb3c8',
      400: '#829ab1',
      500: '#627d98', // Main
      600: '#486581', // Dark
      700: '#334e68',
      800: '#243b53',
      900: '#0F3D5E', // Brand Navy
    },
    // Secondary Palette - SmartProBono Teal
    secondary: {
      50: '#f0fdfa',
      100: '#ccfbf1',
      200: '#99f6e4',
      300: '#5eead4',
      400: '#2dd4bf',
      500: '#14b8a6',
      600: '#1FB6A6', // Brand Teal
      700: '#0f766e',
      800: '#115e59',
      900: '#134e4a',
    },
    // Neutral Palette
    neutral: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a',
    },
    // Semantic Colors
    success: {
      50: '#ecfdf5',
      500: '#10b981',
      600: '#059669',
      700: '#047857',
    },
    warning: {
      50: '#fffbeb',
      500: '#f59e0b',
      600: '#d97706',
      700: '#b45309',
    },
    error: {
      50: '#fef2f2',
      500: '#ef4444',
      600: '#dc2626',
      700: '#b91c1c',
    },
    info: {
      50: '#f0f9ff',
      500: '#06b6d4',
      600: '#0891b2',
      700: '#0e7490',
    },
  },
  
  typography: {
    fontFamily: {
      primary: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      mono: 'JetBrains Mono, "Fira Code", Consolas, monospace',
    },
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
      '5xl': '3rem',    // 48px
      '6xl': '3.5rem',  // 56px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
      black: 900,
    },
    lineHeight: {
      tight: 1.1,
      snug: 1.2,
      normal: 1.5,
      relaxed: 1.6,
      loose: 1.8,
    },
  },
  
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
    20: '5rem',     // 80px
    24: '6rem',     // 96px
    32: '8rem',     // 128px
  },
  
  borderRadius: {
    none: '0',
    sm: '0.25rem',   // 4px
    base: '0.5rem',  // 8px
    md: '0.75rem',   // 12px
    lg: '1rem',      // 16px
    xl: '1.5rem',    // 24px
    '2xl': '2rem',   // 32px
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  },
  
  gradients: {
    primary: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)',
    secondary: 'linear-gradient(135deg, #1FB6A6 0%, #0F3D5E 100%)',
    hero: 'linear-gradient(135deg, #0F3D5E 0%, #1FB6A6 100%)',
    card: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
    overlay: 'linear-gradient(135deg, rgba(15, 61, 94, 0.8) 0%, rgba(31, 182, 166, 0.8) 100%)',
  },
  
  animations: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    },
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    },
  },
  
  breakpoints: {
    xs: '0px',
    sm: '600px',
    md: '900px',
    lg: '1200px',
    xl: '1536px',
  },
};

// Component Variants
export const componentVariants = {
  button: {
    primary: {
      background: designTokens.gradients.primary,
      color: 'white',
      hover: {
        transform: 'translateY(-2px)',
        boxShadow: designTokens.shadows.lg,
      },
    },
    secondary: {
      background: 'transparent',
      color: designTokens.colors.primary[600],
      border: `2px solid ${designTokens.colors.primary[600]}`,
      hover: {
        background: designTokens.colors.primary[50],
        transform: 'translateY(-2px)',
      },
    },
    ghost: {
      background: 'transparent',
      color: designTokens.colors.neutral[600],
      hover: {
        background: designTokens.colors.neutral[100],
      },
    },
  },
  
  card: {
    default: {
      background: 'white',
      borderRadius: designTokens.borderRadius.lg,
      boxShadow: designTokens.shadows.base,
      border: `1px solid ${designTokens.colors.neutral[200]}`,
      hover: {
        boxShadow: designTokens.shadows.lg,
        transform: 'translateY(-4px)',
      },
    },
    elevated: {
      background: 'white',
      borderRadius: designTokens.borderRadius.lg,
      boxShadow: designTokens.shadows.lg,
      border: 'none',
      hover: {
        boxShadow: designTokens.shadows.xl,
        transform: 'translateY(-6px)',
      },
    },
    gradient: {
      background: designTokens.gradients.card,
      borderRadius: designTokens.borderRadius.lg,
      boxShadow: designTokens.shadows.base,
      border: `1px solid ${designTokens.colors.neutral[200]}`,
    },
  },
  
  input: {
    default: {
      borderRadius: designTokens.borderRadius.md,
      border: `1px solid ${designTokens.colors.neutral[300]}`,
      focus: {
        borderColor: designTokens.colors.primary[500],
        boxShadow: `0 0 0 3px ${designTokens.colors.primary[100]}`,
      },
    },
  },
};

// Layout Constants
export const layoutConstants = {
  maxWidth: {
    xs: '100%',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  containerPadding: {
    xs: designTokens.spacing[4],
    sm: designTokens.spacing[6],
    md: designTokens.spacing[8],
    lg: designTokens.spacing[12],
  },
  sectionSpacing: {
    xs: designTokens.spacing[12],
    md: designTokens.spacing[20],
  },
};

export default designTokens;
