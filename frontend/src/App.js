import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import PropTypes from 'prop-types';
import ThemeProvider from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import i18n from './i18n/index';
import WebSocketTestComponent from './components/WebSocketTestComponent';
import { WebSocketProvider } from './contexts/WebSocketContext';
import WebSocketDocPage from './pages/WebSocketDocPage';
import { NotificationProvider } from './contexts/NotificationContext';
import NotificationTestPage from './pages/NotificationTestPage';
import { Box, Toolbar } from '@mui/material';

// Components
import Navigation from './components/Navigation';
import ErrorBoundary from './components/ErrorBoundary';
import LegalAIChat from './components/LegalAIChat';
import LegalAssistantChat from './components/LegalAssistantChat';
import LegalDocumentAnalyzer from './components/LegalDocumentAnalyzer';
import LegalRightsVisualizer from './components/LegalRightsVisualizer';
import PremiumRouteGuard from './components/PremiumRouteGuard';
import ProgressTracker from './components/ProgressTracker';
import SubscriptionPlans from './components/SubscriptionPlans';
import LegalAnalytics from './components/LegalAnalytics';
import IdentityVerification from './components/IdentityVerification';
import FeedbackAnalytics from './components/FeedbackAnalytics';
import DocumentGenerator from './components/DocumentGenerator';
import DocumentAnalyzer from './components/DocumentAnalyzer';
import QueueMonitorDashboard from './components/queue/QueueMonitorDashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';
import RealTimeCaseDashboard from './components/RealTimeCaseDashboard';

// Pages
import HomePage from './pages/HomePage';
import ContractsPage from './pages/ContractsPage';
import Immigration from './pages/Immigration';
import Resources from './pages/Resources';
import RightsPage from './pages/RightsPage';
import Services from './pages/Services';
import Contact from './pages/Contact';
import SettingsPage from './pages/SettingsPage';
import NotFoundPage from './pages/NotFoundPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import DocumentAnalyzerPage from './pages/DocumentAnalyzerPage';
import DocumentGeneratorPage from './pages/DocumentGeneratorPage';
import DocumentFormPage from './pages/DocumentFormPage';
import DocumentPreviewPage from './pages/DocumentPreviewPage';
import DocumentTemplatesPage from './pages/DocumentTemplatesPage';
import EmergencyLegalSupportPage from './pages/EmergencyLegalSupportPage';
import FindLawyerPage from './pages/FindLawyerPage';
import CasesPage from './pages/CasesPage';
import CaseDetailPage from './pages/CaseDetailPage';
import NewCasePage from './pages/NewCasePage';
import SafetyMonitorPage from './pages/SafetyMonitorPage';
import AccessibilityPage from './pages/AccessibilityPage';
import ChatRoomPage from './pages/ChatRoomPage';
import DocumentSuccessPage from './pages/DocumentSuccessPage';

// Layout components for nested routes
const ServicesLayout = () => (
  <div>
    <Outlet />
  </div>
);

const ResourcesLayout = () => (
  <div>
    <Outlet />
  </div>
);

const LegalChatLayout = () => (
  <div>
    <Outlet />
  </div>
);

// Document Templates Layout
const DocumentTemplatesLayout = () => (
  <div>
    <Outlet />
  </div>
);

// Case Management Layout (Requires login)
const CasesLayout = () => (
  <div>
    <Outlet />
  </div>
);

// Chat Room Layout
const ChatRoomLayout = () => (
  <div>
    <Outlet />
  </div>
);

// WebSocket Test component layout
const WebSocketTestLayout = () => (
  <div>
    <WebSocketTestComponent />
  </div>
);

const AppLayout = () => (
  <Box sx={{ display: 'flex' }}>
    <Navigation />
    <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
      <Toolbar />
      <Routes>
        {/* Default route */}
        <Route path="/" element={<Navigate to="/cases" replace />} />
        
        {/* Main app routes */}
        <Route path="/cases/*" element={<CasesLayout />}>
          <Route index element={<RealTimeCaseDashboard />} />
          <Route path="list" element={<CasesPage />} />
          <Route path="new" element={<NewCasePage />} />
          <Route path=":caseId" element={<CaseDetailPage />} />
        </Route>
        
        <Route path="/chat/*" element={<LegalChatLayout />}>
          <Route index element={<LegalAIChat />} />
          <Route path="room/:roomId" element={<ChatRoomPage />} />
          <Route path="legal-assistant" element={<LegalAssistantChat />} />
          <Route path="document-analyzer" element={<LegalDocumentAnalyzer />} />
          <Route path="rights-visualizer" element={<LegalRightsVisualizer />} />
        </Route>
        
        <Route path="/documents/*" element={<DocumentTemplatesLayout />}>
          <Route index element={<DocumentTemplatesPage />} />
          <Route path="analyze" element={<DocumentAnalyzerPage />} />
        </Route>
        
        <Route path="/document-generator" element={<DocumentGeneratorPage />} />
        <Route path="/document-generator/form/:templateId" element={<DocumentFormPage />} />
        <Route path="/document-generator/preview/:templateId" element={<DocumentPreviewPage />} />
        <Route path="/document-generator/success" element={<DocumentSuccessPage />} />
        <Route path="/document-templates" element={<DocumentTemplatesPage />} />
        
        <Route path="/resources/*" element={<ResourcesLayout />}>
          <Route index element={<Resources />} />
          <Route path="rights" element={<RightsPage />} />
        </Route>
        
        <Route path="/services/*" element={<ServicesLayout />}>
          <Route index element={<Services />} />
          <Route path="contracts" element={<ContractsPage />} />
          <Route path="immigration" element={<Immigration />} />
          <Route path="emergency" element={<EmergencyLegalSupportPage />} />
          <Route path="find-lawyer" element={<FindLawyerPage />} />
        </Route>
        
        {/* Auth routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/profile" element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        } />
        
        {/* Protected routes */}
        <Route path="/settings" element={
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        } />
        <Route path="/queue-monitor" element={
          <ProtectedRoute>
            <QueueMonitorDashboard />
          </ProtectedRoute>
        } />
        <Route path="/safety-monitor/:caseId" element={
          <ProtectedRoute>
            <SafetyMonitorPage />
          </ProtectedRoute>
        } />
        
        {/* Utility routes */}
        <Route path="/contact" element={<Contact />} />
        <Route path="/accessibility" element={<AccessibilityPage />} />
        <Route path="/websocket-test" element={<WebSocketTestLayout />} />
        <Route path="/notification-test" element={<NotificationTestPage />} />
        
        {/* Catch all route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Box>
  </Box>
);

const App = () => {
  const isPremium = false;

  // Initialize i18n language and direction
  useEffect(() => {
    if (i18n && typeof i18n.language === 'string') {
      document.documentElement.lang = i18n.language;
      document.documentElement.dir = i18n.language === 'ar' ? 'rtl' : 'ltr';
    }
  }, []);

  // Protected route component
  const ProtectedRouteComponent = ({ children }) => {
    const isAuthenticated = localStorage.getItem('authToken') !== null;
    return isAuthenticated ? (
      children
    ) : (
      <Navigate to="/login" replace state={{ from: window.location.pathname }} />
    );
  };

  ProtectedRouteComponent.propTypes = {
    children: PropTypes.node.isRequired,
  };

  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <ThemeProvider>
        <AuthProvider>
          <WebSocketProvider>
            <NotificationProvider>
              <ErrorBoundary>
                <Routes>
                  <Route path="/*" element={<AppLayout />} />
                </Routes>
              </ErrorBoundary>
            </NotificationProvider>
          </WebSocketProvider>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
};

export default App;
