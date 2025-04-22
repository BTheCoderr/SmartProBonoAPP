import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { I18nextProvider } from 'react-i18next';
import { theme } from './components/theme';
import i18n from './translations/i18n';

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

// Layout components for nested routes
const ServicesLayout = () => (
  <div>
    <Navigation />
    <Routes>
      <Route index element={<Services />} />
      <Route path="contracts/*" element={<ContractsPage />} />
      <Route path="immigration/*" element={<Immigration />} />
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
  <div>
    <Navigation />
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
  <div>
    <Navigation />
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
      <ThemeProvider theme={theme}>
        <HashRouter 
          future={{ 
            v7_startTransition: true,
            v7_relativeSplatPath: true 
          }}
        >
          <ErrorBoundary>
            <div className="App">
              <Navigation />
              <Routes>
                {/* Main routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/services/*" element={<ServicesLayout />} />
                <Route path="/resources/*" element={<ResourcesLayout />} />
                <Route path="/contact" element={<Contact />} />
                
                {/* Document Management route */}
                <Route path="/documents" element={<DocumentsPage />} />
                
                {/* Legal Chat route */}
                <Route path="/legal-chat/*" element={<LegalChatLayout />} />
                
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
                <Route path="/subscription" element={<SubscriptionPlans />} />
                
                {/* Catch-all route for 404 */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </div>
          </ErrorBoundary>
        </HashRouter>
      </ThemeProvider>
    </I18nextProvider>
  );
};

export default App;
