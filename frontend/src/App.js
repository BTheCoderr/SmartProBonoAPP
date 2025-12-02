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

// Components - Commented out (not needed for minimal startup)
// import LegalAIChat from './components/LegalAIChat';
// import PremiumRouteGuard from './components/PremiumRouteGuard';
// import LegalAnalytics from './components/LegalAnalytics';
// import FeedbackAnalytics from './components/FeedbackAnalytics';

// Pages - Essential (Active)
import About from './pages/About';
import Contact from './pages/Contact';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';
import TermsOfServicePage from './pages/TermsOfServicePage';

// Pages - Optional (Commented out but available for re-enabling)
// import ContractsPage from './pages/ContractsPage';
// import Immigration from './pages/Immigration';
// import Resources from './pages/Resources';
// import RightsPage from './pages/RightsPage';
// import Services from './pages/Services';
// import VirtualParalegalPage from './pages/VirtualParalegalPage';
// import AIVirtualParalegal from './components/EnhancedAIVirtualParalegal';
// import ClientPortal from './pages/ClientPortal';
// import LawyerDashboard from './pages/LawyerDashboard';
// import BondsmanDashboard from './pages/BondsmanDashboard';
// import DocumentsPage from './pages/DocumentsPage';
// import ExpertHelpPage from './pages/ExpertHelpPage';
// import AccessibilityPage from './pages/AccessibilityPage';
// import SitemapPage from './pages/SitemapPage';
// import VolunteerFormPage from './pages/VolunteerFormPage';
// import LegalHelpFormPage from './pages/LegalHelpFormPage';

// Core layout components
import Header from './components/Header';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop';

// Page components - Essential (Active)
import HomePage from './pages/HomePage';
import Dashboard from './pages/EnhancedDashboard';
import LegalAIChatPage from './pages/LegalAIChatPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';
import DocumentScanPage from './pages/DocumentScanPage';
import LanguageSwitcher from './components/LanguageSwitcher';

// Page components - Optional (Commented out but available for re-enabling)
// import FormsDashboard from './pages/FormsDashboard';
// import ProfilePage from './pages/ProfilePage';
// import AdminDashboard from './pages/AdminDashboard';
// import UnauthorizedPage from './pages/UnauthorizedPage';
// import StatusPage from './pages/StatusPage';
// import HelpPage from './pages/HelpPage';
// import BugReportPage from './pages/BugReportPage';
// import FeatureRequestPage from './pages/FeatureRequestPage';
// import PartnersPage from './pages/PartnersPage';
// import PressPage from './pages/PressPage';
// import CareersPage from './pages/CareersPage';
// import TeamPage from './pages/TeamPage';
// import OurMissionPage from './pages/OurMissionPage';
// import GlossaryPage from './pages/ComprehensiveGlossaryPage';
// import FAQPage from './pages/FAQPage';
// import BlogPage from './pages/BlogPage';
// import LiveChatPage from './pages/LiveChatPage';
// import DocumentGenerator from './components/DocumentGenerator';
// import PDFGenerator from './components/documents/PDFGenerator';
// import ExpungementWizard from './components/ExpungementWizard';
// import DocumentChecklistPage from './pages/DocumentChecklistPage';
// import SafetyCheckPage from './pages/SafetyCheckPage';
// import LegalToolsPage from './pages/LegalToolsPage';
// import ImmigrationResourcesPage from './pages/ImmigrationResourcesPage';
// import ImmigrationRightsPage from './pages/ImmigrationRightsPage';
// import ExternalResourcesPage from './pages/ExternalResourcesPage';
// import LegalGuidesPage from './pages/LegalGuidesPage';
// import CaseLawPage from './pages/CaseLawPage';

// Protected route wrapper - DISABLED FOR DEVELOPMENT
const ProtectedRoute = ({ children }) => {
  // During development, always allow access without authentication
  console.log('Protected route accessed - authentication disabled for development');
  return children;
};

// Admin route wrapper - DISABLED FOR DEVELOPMENT (commented out - not used in minimal startup)
/*
const AdminRoute = ({ children }) => {
  // During development, always allow access without authentication
  console.log('Admin route accessed - authentication disabled for development');
  return children;
};
*/

// Layout components for nested routes - Commented out (available for re-enabling)
/*
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
      <Route path="checklist/:type" element={<DocumentChecklistPage />} />
      <Route path="immigration" element={<ImmigrationResourcesPage />} />
      <Route path="external" element={<ExternalResourcesPage />} />
      <Route path="guides" element={<LegalGuidesPage />} />
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
*/


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
  // const { user } = useAuth();
  
  // Use user to conditionally show content or features
  // const showPremiumFeatures = user && user.isPremium;
  
  // Authentication status for conditional rendering

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
            {/* ============================================ */}
            {/* ESSENTIAL ROUTES - Minimal Startup (8-10 pages) */}
            {/* ============================================ */}
            
            {/* Core Pages */}
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            
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
            
            {/* Legal Requirements */}
            <Route path="/privacy" element={<PrivacyPolicyPage />} />
            <Route path="/terms" element={<TermsOfServicePage />} />
            
            {/* Error Handling */}
            <Route path="*" element={<NotFoundPage />} />
            
            {/* ============================================ */}
            {/* OPTIONAL ROUTES - Commented out but available */}
            {/* Uncomment routes below to enable additional features */}
            {/* ============================================ */}
            
            {/* 
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
            
            <Route path="/chat" element={<LiveChatPage />} />
            
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

            <Route path="/services/*" element={<ServicesLayout />} />
            <Route path="/resources/*" element={<ResourcesLayout />} />
            
            <Route path="/legal-tools" element={<LegalToolsPage />} />
            <Route path="/generate-document" element={<PDFGenerator />} />
            <Route path="/safety-check" element={<SafetyCheckPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/expert-help" element={<ExpertHelpPage />} />
            <Route path="/caselaw" element={<CaseLawPage />} />
            
            <Route 
              path="/virtual-paralegal" 
              element={
                <ProtectedRoute>
                  <VirtualParalegalPage />
                </ProtectedRoute>
              } 
            />
            
            <Route 
              path="/ai-virtual-paralegal" 
              element={<AIVirtualParalegal />}
            />
            
            <Route 
              path="/client-portal" 
              element={<ClientPortal />}
            />
            
            <Route 
              path="/lawyer-dashboard" 
              element={<LawyerDashboard />}
            />
            
            <Route 
              path="/bondsman-dashboard" 
              element={<BondsmanDashboard />}
            />
            
            <Route path="/services" element={<Services />} />
            <Route path="/status" element={<StatusPage />} />
            <Route path="/help" element={<HelpPage />} />
            <Route path="/bug-report" element={<BugReportPage />} />
            <Route path="/feature-request" element={<FeatureRequestPage />} />
            <Route path="/partners" element={<PartnersPage />} />
            <Route path="/press" element={<PressPage />} />
            <Route path="/careers" element={<CareersPage />} />
            <Route path="/team" element={<TeamPage />} />
            <Route path="/mission" element={<OurMissionPage />} />
            <Route path="/rights" element={<RightsPage />} />
            <Route path="/accessibility" element={<AccessibilityPage />} />
            <Route path="/sitemap" element={<SitemapPage />} />
            <Route path="/volunteer" element={<VolunteerFormPage />} />
            <Route path="/get-legal-help" element={<LegalHelpFormPage />} />
            <Route path="/rights/immigration" element={<ImmigrationRightsPage />} />
            <Route path="/glossary" element={<GlossaryPage />} />
            <Route path="/faq" element={<FAQPage />} />
            <Route path="/blog" element={<BlogPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            */}
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
    // Available routes for debugging (commented out to reduce console noise)
    // console.log('Available routes:', routes.map(route => route.path).join(', '));
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
