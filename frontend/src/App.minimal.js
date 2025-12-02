import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { Toaster } from 'react-hot-toast';
import { I18nextProvider } from 'react-i18next';
import { SnackbarProvider } from 'notistack';
import ReactGA from 'react-ga4';
import ErrorBoundary from './components/ErrorBoundary';
import theme from './theme';
import { AuthProvider } from './context/AuthContext';
import { AnalyticsProvider } from './contexts/AnalyticsContext';
import i18n from './i18n';

// Core layout components
import Header from './components/Header';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop';
import LanguageSwitcher from './components/LanguageSwitcher';

// ESSENTIAL PAGES ONLY - Minimal Startup
import HomePage from './pages/HomePage';
import LegalAIChatPage from './pages/LegalAIChatPage';
import DocumentScanPage from './pages/DocumentScanPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/EnhancedDashboard';
import About from './pages/About';
import Contact from './pages/Contact';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';
import TermsOfServicePage from './pages/TermsOfServicePage';
import NotFoundPage from './pages/NotFoundPage';

// Protected route wrapper - DISABLED FOR DEVELOPMENT
const ProtectedRoute = ({ children }) => {
  console.log('Protected route accessed - authentication disabled for development');
  return children;
};

const LoadingFallback = () => (
  <div>Loading...</div>
);

const trackPageView = (location) => {
  ReactGA.send({ hitType: "pageview", page: location.pathname + location.search });
};

const PageTracker = () => {
  const location = useLocation();
  
  useEffect(() => {
    trackPageView(location);
  }, [location]);
  
  return null;
};

function AppContent() {
  return (
    <>
      <Header />
      <PageTracker />
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', padding: '0 20px' }}>
        <LanguageSwitcher />
      </div>
      <main style={{ minHeight: 'calc(100vh - 64px - 50px)', paddingTop: '20px', paddingBottom: '40px' }}>
        <React.Suspense fallback={<LoadingFallback />}>
          <Routes>
            {/* ESSENTIAL ROUTES ONLY - Minimal Startup */}
            <Route path="/" element={<HomePage />} />
            
            {/* Core Features */}
            <Route path="/legal-chat" element={<LegalAIChatPage />} />
            <Route 
              path="/scan-document" 
              element={
                <ProtectedRoute>
                  <DocumentScanPage />
                </ProtectedRoute>
              } 
            />
            
            {/* Auth */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            {/* Dashboard */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Basic Pages */}
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            
            {/* Legal Requirements */}
            <Route path="/privacy" element={<PrivacyPolicyPage />} />
            <Route path="/terms" element={<TermsOfServicePage />} />
            
            {/* Error Handling */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </React.Suspense>
      </main>
      <Footer />
      <Toaster position="top-center" />
    </>
  );
}

function App() {
  useEffect(() => {
    if (process.env.REACT_APP_GA_TRACKING_ID) {
      ReactGA.initialize(process.env.REACT_APP_GA_TRACKING_PAGE);
      console.log('Analytics initialized');
    }
  }, []);
  
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <I18nextProvider i18n={i18n}>
          <SnackbarProvider maxSnack={3}>
            <Router
              future={{
                v7_startTransition: true,
                v7_relativeSplatPath: true,
              }}
            >
              <ScrollToTop />
              <AuthProvider>
                <AnalyticsProvider>
                  <AppContent />
                </AnalyticsProvider>
              </AuthProvider>
            </Router>
          </SnackbarProvider>
        </I18nextProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;

