import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { Toaster } from 'react-hot-toast';
import { I18nextProvider } from 'react-i18next';
import { SnackbarProvider } from 'notistack';
import ReactGA from 'react-ga4';
import ErrorBoundary from './components/ErrorBoundary';
import theme from './theme';
import routes from './routes';
import { AuthProvider, useAuth } from './context/AuthContext';
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
import DocumentsPage from './pages/DocumentsPage';
import ExpertHelpPage from './pages/ExpertHelpPage';
import About from './pages/About';
import Contact from './pages/Contact';

// Core layout components
import Header from './components/Header';
import Footer from './components/Footer';

// Page components
import HomePage from './pages/HomePage';
import Dashboard from './pages/Dashboard';
import FormsDashboard from './pages/FormsDashboard';
import LegalAIChatPage from './pages/LegalAIChatPage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AdminDashboard from './pages/AdminDashboard';
import NotFoundPage from './pages/NotFoundPage';
import UnauthorizedPage from './pages/UnauthorizedPage';

// New components
import DocumentGenerator from './components/DocumentGenerator';
import ExpungementWizard from './components/ExpungementWizard';
import LanguageSwitcher from './components/LanguageSwitcher';
import DocumentScanPage from './pages/DocumentScanPage';

// Protected route wrapper - updated to use the current AuthContext implementation
const ProtectedRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: window.location.pathname }} replace />;
  }
  
  return children;
};

// Admin route wrapper - updated to use the current AuthContext implementation
const AdminRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!isAuthenticated || user?.role !== 'admin') {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return children;
};

// Layout components for nested routes
const ServicesLayout = () => (
  <div style={{ height: '100vh', overflow: 'auto' }}>
    <Routes>
      <Route index element={<Services />} />
      <Route path="contracts/*" element={
        <ProtectedRoute>
          <ContractsPage />
        </ProtectedRoute>
      } />
      <Route path="immigration/*" element={
        <ProtectedRoute>
          <Immigration />
        </ProtectedRoute>
      } />
      <Route path="virtual-paralegal" element={
        <ProtectedRoute>
          <VirtualParalegalPage />
        </ProtectedRoute>
      } />
      <Route 
        path="analytics" 
        element={
          <ProtectedRoute>
            <PremiumRouteGuard isPremium={false}>
              <LegalAnalytics />
            </PremiumRouteGuard>
          </ProtectedRoute>
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
  <div>Loading...</div>
);

const trackPageView = (location) => {
  ReactGA.send({ hitType: "pageview", page: location.pathname + location.search });
};

// Page tracker component
const PageTracker = () => {
  const location = useLocation();
  
  useEffect(() => {
    trackPageView(location);
  }, [location]);
  
  return null;
};

function AppContent() {
  const { user, isAuthenticated } = useAuth();
  
  // Use user to conditionally show content or features
  const showPremiumFeatures = user && user.isPremium;

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
            <Route path="/" element={<HomePage />} />
            
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/forms" 
              element={
                <ProtectedRoute>
                  <FormsDashboard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/forms/:formType" 
              element={
                <ProtectedRoute>
                  <DocumentGenerator />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/expungement-toolkit" 
              element={
                <ProtectedRoute>
                  <ExpungementWizard />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/chat" 
              element={
                <ProtectedRoute>
                  <LegalAIChatPage />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/admin" 
              element={
                <AdminRoute>
                  <AdminDashboard />
                </AdminRoute>
              } 
            />

            {/* Using the layout components */}
            <Route path="/services/*" element={<ServicesLayout />} />
            <Route path="/resources/*" element={<ResourcesLayout />} />
            
            {/* MVP Critical Routes - Ensure these are accessible without authentication */}
            <Route path="/legal-chat" element={<LegalAIChatPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/expert-help" element={<ExpertHelpPage />} />
            
            {/* Additional MVP routes */}
            <Route path="/about" element={<About />} />
            <Route path="/services" element={<Services />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/contact" element={<Contact />} />
            
            {/* Conditionally render premium features */}
            <Route 
              path="/legal-chat/premium" 
              element={showPremiumFeatures ? <LegalChatLayout /> : <Navigate to="/subscription" />} 
            />
            
            <Route path="/resources" element={<Resources />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            <Route 
              path="/scan-document" 
              element={
                <ProtectedRoute>
                  <DocumentScanPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/document-scan" 
              element={
                <ProtectedRoute>
                  <DocumentScanPage />
                </ProtectedRoute>
              } 
            />
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
  // Initialize analytics
  useEffect(() => {
    // Initialize GA
    if (process.env.REACT_APP_GA_TRACKING_ID) {
      ReactGA.initialize(process.env.REACT_APP_GA_TRACKING_ID);
      console.log('Analytics initialized');
    }
    
    // Apply routes configuration
    console.log('Available routes:', routes.map(route => route.path).join(', '));
  }, []);
  
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <I18nextProvider i18n={i18n}>
          <SnackbarProvider maxSnack={3}>
            <Router>
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
