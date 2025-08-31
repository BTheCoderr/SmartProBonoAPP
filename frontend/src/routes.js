import React from 'react';
import { Navigate } from 'react-router-dom';

// Lazy load components
const About = React.lazy(() => import('./pages/About'));
const LoginPage = React.lazy(() => import('./pages/LoginPage'));
const RegisterPage = React.lazy(() => import('./pages/RegisterPage'));
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const AdminDashboard = React.lazy(() => import('./pages/AdminDashboard'));
const LawyerDashboard = React.lazy(() => import('./pages/LawyerDashboard'));
const FormsDashboard = React.lazy(() => import('./pages/FormsDashboard'));
const AnalyticsDashboard = React.lazy(() => import('./pages/AnalyticsDashboard'));
const ImmigrationDashboard = React.lazy(() => import('./pages/ImmigrationDashboard'));
const AdminNotificationDashboard = React.lazy(() => import('./pages/AdminNotificationDashboard'));
const AuditDashboard = React.lazy(() => import('./components/AuditDashboard'));
const DocumentsPage = React.lazy(() => import('./pages/DocumentsPage'));
const ContractsPage = React.lazy(() => import('./pages/ContractsPage'));
const VirtualParalegalPage = React.lazy(() => import('./pages/VirtualParalegalPage'));
const ProfilePage = React.lazy(() => import('./pages/ProfilePage'));
const ExpungementPage = React.lazy(() => import('./pages/ExpungementPage'));
const FormsIndexPage = React.lazy(() => import('./pages/FormsIndexPage'));
const Resources = React.lazy(() => import('./pages/Resources'));
const Services = React.lazy(() => import('./pages/Services'));
const RightsPage = React.lazy(() => import('./pages/RightsPage'));
const ProceduresPage = React.lazy(() => import('./pages/ProceduresPage'));
const Contact = React.lazy(() => import('./pages/Contact'));
const LegalAIChat = React.lazy(() => import('./components/LegalAIChat'));
const BetaLandingPage = React.lazy(() => import('./pages/BetaLandingPage'));
const BetaConfirm = React.lazy(() => import('./pages/BetaConfirm'));
const BusinessModel = React.lazy(() => import('./pages/BusinessModel'));
const ThankYouPage = React.lazy(() => import('./pages/ThankYouPage'));
const ResetPasswordPage = React.lazy(() => import('./pages/ResetPasswordPage'));
const ForgotPasswordPage = React.lazy(() => import('./pages/ForgotPasswordPage'));
const UnauthorizedPage = React.lazy(() => import('./pages/UnauthorizedPage'));
const NotFoundPage = React.lazy(() => import('./pages/NotFoundPage'));
const ExpertHelpPage = React.lazy(() => import('./pages/ExpertHelpPage'));
const AuthTestPage = React.lazy(() => import('./pages/AuthTestPage'));
const DesignSystemTest = React.lazy(() => import('./components/DesignSystemTest'));
const FeatureRequestPage = React.lazy(() => import('./pages/FeatureRequestPage'));
const BugReportPage = React.lazy(() => import('./pages/BugReportPage'));
const HelpPage = React.lazy(() => import('./pages/HelpPage'));
const StatusPage = React.lazy(() => import('./pages/StatusPage'));
const GlossaryPage = React.lazy(() => import('./pages/GlossaryPage'));
const ImmigrationResourcesPage = React.lazy(() => import('./pages/ImmigrationResourcesPage'));
const LegalGuidesPage = React.lazy(() => import('./pages/LegalGuidesPage'));
const ExternalResourcesPage = React.lazy(() => import('./pages/ExternalResourcesPage'));
const ComplianceScannerPage = React.lazy(() => import('./pages/ComplianceScannerPage'));
const PolicyGeneratorPage = React.lazy(() => import('./pages/PolicyGeneratorPage'));
const RiskAssessmentPage = React.lazy(() => import('./pages/RiskAssessmentPage'));

const routes = [
  { path: '/', element: <BetaLandingPage /> },
  { path: '/about', element: <About /> },
  { path: '/login', element: <LoginPage /> },
  { path: '/register', element: <RegisterPage /> },
  { path: '/dashboard', element: <Dashboard /> },
  { path: '/admin-dashboard', element: <AdminDashboard /> },
  { path: '/lawyer-dashboard', element: <LawyerDashboard /> },
  { path: '/forms-dashboard', element: <FormsDashboard /> },
  { path: '/analytics-dashboard', element: <AnalyticsDashboard /> },
  { path: '/immigration-dashboard', element: <ImmigrationDashboard /> },
  { path: '/admin-notifications', element: <AdminNotificationDashboard /> },
  { path: '/audit-dashboard', element: <AuditDashboard /> },
  { path: '/documents', element: <DocumentsPage /> },
  { path: '/contracts', element: <ContractsPage /> },
  { path: '/virtual-paralegal', element: <VirtualParalegalPage /> },
  { path: '/profile', element: <ProfilePage /> },
  { path: '/expungement', element: <ExpungementPage /> },
  { path: '/forms', element: <FormsIndexPage /> },
  { path: '/resources', element: <Resources /> },
  { path: '/services', element: <Services /> },
  { path: '/rights', element: <RightsPage /> },
  { path: '/procedures', element: <ProceduresPage /> },
  { path: '/contact', element: <Contact /> },
  { path: '/legal-chat', element: <LegalAIChat /> },
  { path: '/beta/confirm/:token', element: <BetaConfirm /> },
  { path: '/business-model', element: <BusinessModel /> },
  { path: '/thank-you', element: <ThankYouPage /> },
  { path: '/reset-password', element: <ResetPasswordPage /> },
  { path: '/forgot-password', element: <ForgotPasswordPage /> },
  { path: '/unauthorized', element: <UnauthorizedPage /> },
  { path: '/not-found', element: <NotFoundPage /> },
  { path: '/expert-help', element: <ExpertHelpPage /> },
  { path: '/auth-test', element: <AuthTestPage /> },
  { path: '/design-test', element: <DesignSystemTest /> },
  { path: '/feature-request', element: <FeatureRequestPage /> },
  { path: '/bug-report', element: <BugReportPage /> },
  { path: '/help', element: <HelpPage /> },
  { path: '/status', element: <StatusPage /> },
  { path: '/glossary', element: <GlossaryPage /> },
  { path: '/resources/immigration', element: <ImmigrationResourcesPage /> },
  { path: '/resources/guides', element: <LegalGuidesPage /> },
  { path: '/resources/external', element: <ExternalResourcesPage /> },
  { path: '/compliance-scanner', element: <ComplianceScannerPage /> },
  { path: '/policy-generator', element: <PolicyGeneratorPage /> },
  { path: '/risk-assessment', element: <RiskAssessmentPage /> },
  { path: '*', element: <Navigate to="/not-found" replace /> },
];

export default routes; 