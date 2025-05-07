import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { I18nextProvider } from 'react-i18next';
import { SnackbarProvider } from 'notistack';
import ReactGA from 'react-ga4';
import ErrorBoundary from './components/ErrorBoundary';
import theme from './theme';
import routes from './routes';
import { AuthProvider } from './context/AuthContext';
import { AnalyticsProvider } from './contexts/AnalyticsContext';
import i18n from './translations/i18n';

// Components
import LegalAIChat from './components/LegalAIChat';
import PremiumRouteGuard from './components/PremiumRouteGuard';
import LegalAnalytics from './components/LegalAnalytics';
import FeedbackAnalytics from './components/FeedbackAnalytics';

// Pages
import ContractsPage from './pages/ContractsPage';
import Immigration from './pages/Immigration';
import Resources from './pages/Resources';
import RightsPage from './pages/RightsPage';
import Services from './pages/Services';
import VirtualParalegalPage from './pages/VirtualParalegalPage';

// Configure React Router future flags
const router = {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true
  },
};

// Layout components for nested routes
const ServicesLayout = () => (
  <div style={{ height: '100vh', overflow: 'auto' }}>
    <Routes>
      <Route index element={<Services />} />
      <Route path="contracts/*" element={<ContractsPage />} />
      <Route path="immigration/*" element={<Immigration />} />
      <Route path="virtual-paralegal" element={<VirtualParalegalPage />} />
      <Route 
        path="analytics" 
        element={
          <PremiumRouteGuard isPremium={false}>
            <LegalAnalytics />
          </PremiumRouteGuard>
        } 
      />
    </Routes>
  </div>
);

const ResourcesLayout = () => (
  <div style={{ height: '100vh', overflow: 'auto' }}>
    <Routes>
      <Route index element={<Resources />} />
      <Route path="rights" element={<RightsPage />} />
      <Route 
        path="premium-guides" 
        element={
          <PremiumRouteGuard isPremium={false}>
            <Resources type="premium" />
          </PremiumRouteGuard>
        } 
      />
    </Routes>
  </div>
);

const LegalChatLayout = () => (
  <div style={{ height: '100vh', overflow: 'auto' }}>
    <Routes>
      <Route index element={<LegalAIChat />} />
      <Route 
        path="premium" 
        element={
          <PremiumRouteGuard isPremium={false}>
            <LegalAIChat premium={true} />
          </PremiumRouteGuard>
        } 
      />
      <Route 
        path="feedback" 
        element={
          <PremiumRouteGuard isPremium={false}>
            <FeedbackAnalytics />
          </PremiumRouteGuard>
        } 
      />
    </Routes>
  </div>
);

const LoadingFallback = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
    <CircularProgress />
  </Box>
);

const trackPageView = (location) => {
  ReactGA.send({ hitType: "pageview", page: location.pathname + location.search });
};

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <I18nextProvider i18n={i18n}>
          <SnackbarProvider maxSnack={3}>
            <BrowserRouter future={router.future}>
              <AuthProvider>
                <AnalyticsProvider>
                  <Suspense fallback={<LoadingFallback />}>
                    <Routes>
                      {routes.map((route) => (
                        <Route
                          key={route.path}
                          path={route.path}
                          element={route.element}
                        />
                      ))}
                    </Routes>
                  </Suspense>
                </AnalyticsProvider>
              </AuthProvider>
            </BrowserRouter>
          </SnackbarProvider>
        </I18nextProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
