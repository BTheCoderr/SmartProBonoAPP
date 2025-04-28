import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { I18nextProvider } from 'react-i18next';
import legalTheme from './theme/legalTheme';
import i18n from './translations/i18n';

// Auth Context
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

// Components
import Navigation from './components/Navigation';
import ErrorBoundary from './components/ErrorBoundary';
import LegalAIChat from './components/LegalAIChat';
import PremiumRouteGuard from './components/PremiumRouteGuard';
import ProgressTracker from './components/ProgressTracker';
import SubscriptionPlans from './components/SubscriptionPlans';
import LegalAnalytics from './components/LegalAnalytics';
import IdentityVerification from './components/IdentityVerification';
import FeedbackAnalytics from './components/FeedbackAnalytics';
import ScanDocument from './components/ScanDocument';
import WebSocketClient from './components/WebSocketClient';

// Pages
import HomePage from './pages/HomePage';
import ContractsPage from './pages/ContractsPage';
import Immigration from './pages/Immigration';
import Resources from './pages/Resources';
import RightsPage from './pages/RightsPage';
import Services from './pages/Services';
import Contact from './pages/Contact';
import NotFoundPage from './pages/NotFoundPage';
import DocumentsPage from './pages/DocumentsPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import UnauthorizedPage from './pages/UnauthorizedPage';
import AdminDashboard from './pages/AdminDashboard';
import LawyerDashboard from './pages/LawyerDashboard';
import ExpungementPage from './pages/ExpungementPage';
import ScannerTestPage from './pages/ScannerTestPage';
import ImmigrationDashboard from './pages/ImmigrationDashboard';
import VirtualParalegalPage from './pages/VirtualParalegalPage';
import ThankYouPage from './pages/ThankYouPage';
import OnboardingPage from './pages/OnboardingPage';
import SmallClaimsComplaintForm from './pages/SmallClaimsComplaintForm';
import FormsIndexPage from './pages/FormsIndexPage';
import EvictionResponseForm from './pages/EvictionResponseForm';

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

const App = () => {
  // In a real app, you would get this from your auth/subscription state
  const isPremium = false;

  return (
    <I18nextProvider i18n={i18n}>
      <ThemeProvider theme={legalTheme}>
        <AuthProvider>
          {/* Add WebSocketClient here to handle socket connections */}
          <WebSocketClient />
          <HashRouter 
            future={{ 
              v7_startTransition: true,
              v7_relativeSplatPath: true 
            }}
          >
            <ErrorBoundary>
              <div className="App" style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navigation />
                <div style={{ flex: 1, overflow: 'auto' }}>
                  <Routes>
                    {/* Main routes */}
                    <Route path="/" element={<HomePage />} />
                    <Route path="/thank-you" element={<ThankYouPage />} />
                    <Route path="/onboarding" element={<OnboardingPage />} />
                    <Route path="/contracts" element={<ContractsPage />} />
                    <Route path="/rights" element={<RightsPage />} />
                    <Route path="/rights/:categorySlug" element={<RightsPage />} />
                    <Route path="/services/*" element={<ServicesLayout />} />
                    <Route path="/virtual-paralegal" element={<VirtualParalegalPage />} />
                    <Route path="/resources/*" element={<ResourcesLayout />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="/immigration" element={<Immigration />} />
                    <Route path="/expungement" element={<ExpungementPage />} />
                    <Route path="/scanner-test" element={<ScannerTestPage />} />
                    
                    {/* Make ScanDocument publicly accessible for testing */}
                    <Route path="/scan-document" element={<ScanDocument />} />
                    
                    {/* Legal Forms - publicly accessible for now */}
                    <Route path="/forms" element={<FormsIndexPage />} />
                    <Route path="/forms/small-claims" element={<SmallClaimsComplaintForm />} />
                    <Route path="/forms/eviction-response" element={<EvictionResponseForm />} />
                    
                    {/* Authentication routes */}
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/unauthorized" element={<UnauthorizedPage />} />
                    
                    {/* Protected routes */}
                    <Route element={<ProtectedRoute />}>
                      <Route path="/profile" element={<ProfilePage />} />
                      
                      {/* Document Management route - requires authentication */}
                      <Route path="/documents" element={<DocumentsPage />} />
                      
                      {/* Immigration Dashboard - requires authentication */}
                      <Route path="/immigration-dashboard" element={<ImmigrationDashboard />} />
                      
                      {/* Scan Document route commented out - now public above
                      <Route path="/scan-document" element={<ScanDocument />} />
                      */}
                      
                      {/* Identity Verification route */}
                      <Route 
                        path="/verify" 
                        element={
                          <PremiumRouteGuard isPremium={isPremium}>
                            <IdentityVerification />
                          </PremiumRouteGuard>
                        } 
                      />

                      {/* Progress and subscription routes */}
                      <Route 
                        path="/progress" 
                        element={
                          <PremiumRouteGuard isPremium={isPremium}>
                            <ProgressTracker />
                          </PremiumRouteGuard>
                        } 
                      />
                    </Route>

                    {/* Lawyer-specific routes */}
                    <Route element={<ProtectedRoute requiredRole="lawyer" />}>
                      <Route path="/lawyer-dashboard" element={<LawyerDashboard />} />
                      {/* Add other lawyer-specific routes as needed */}
                    </Route>

                    {/* Admin-specific routes */}
                    <Route element={<ProtectedRoute requiredRole="admin" />}>
                      <Route path="/admin-dashboard" element={<AdminDashboard />} />
                      {/* Add other admin-specific routes as needed */}
                    </Route>
                    
                    {/* Legal Chat route */}
                    <Route path="/legal-chat/*" element={<LegalChatLayout />} />
                    
                    {/* Subscription route - publicly accessible */}
                    <Route path="/subscription" element={<SubscriptionPlans />} />
                    
                    {/* Catch-all route for 404 */}
                    <Route path="*" element={<NotFoundPage />} />
                  </Routes>
                </div>
              </div>
            </ErrorBoundary>
          </HashRouter>
        </AuthProvider>
      </ThemeProvider>
    </I18nextProvider>
  );
};

export default App;
