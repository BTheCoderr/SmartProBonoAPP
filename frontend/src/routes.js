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
const DocumentScanPage = React.lazy(() => import('./pages/DocumentScanPage'));
// Connect to existing pages instead of creating new ones
const DocumentGenerationPage = React.lazy(() => import('./pages/DocumentGenerationPage'));
const DocumentScannerPage = React.lazy(() => import('./pages/ScanDocument'));
const KnowYourRightsPage = React.lazy(() => import('./pages/RightsPage'));
const LegalTemplatesPage = React.lazy(() => import('./pages/LegalTemplatesPage'));
const EducationalContentPage = React.lazy(() => import('./pages/EducationalContentPage'));
const FAQPage = React.lazy(() => import('./pages/FAQPage'));
const BlogPage = React.lazy(() => import('./pages/BlogPage'));
const AboutUsPage = React.lazy(() => import('./pages/About'));
const OurMissionPage = React.lazy(() => import('./pages/OurMissionPage'));
const TeamPage = React.lazy(() => import('./pages/TeamPage'));
const CareersPage = React.lazy(() => import('./pages/CareersPage'));
const PressPage = React.lazy(() => import('./pages/PressPage'));
const PartnersPage = React.lazy(() => import('./pages/PartnersPage'));
const HelpCenterPage = React.lazy(() => import('./pages/HelpPage'));
const LiveChatPage = React.lazy(() => import('./pages/LiveChatPage'));
const PrivacyPolicyPage = React.lazy(() => import('./pages/PrivacyPolicyPage'));
const TermsOfServicePage = React.lazy(() => import('./pages/TermsOfServicePage'));
const AccessibilityPage = React.lazy(() => import('./pages/AccessibilityPage'));
const SitemapPage = React.lazy(() => import('./pages/SitemapPage'));

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
  { path: '/status', element: <StatusPage /> },
  { path: '/glossary', element: <GlossaryPage /> },
  { path: '/resources/immigration', element: <ImmigrationResourcesPage /> },
  { path: '/resources/guides', element: <LegalGuidesPage /> },
  { path: '/resources/external', element: <ExternalResourcesPage /> },
  { path: '/compliance-scanner', element: <ComplianceScannerPage /> },
  { path: '/policy-generator', element: <PolicyGeneratorPage /> },
  { path: '/risk-assessment', element: <RiskAssessmentPage /> },
  // Service pages
  { path: '/document-generation', element: <DocumentGenerationPage /> },
  { path: '/document-scanner', element: <DocumentScannerPage /> },
  { path: '/immigration', element: <ImmigrationResourcesPage /> },
  // Resource pages
  { path: '/know-your-rights', element: <KnowYourRightsPage /> },
  { path: '/legal-templates', element: <LegalTemplatesPage /> },
  { path: '/educational-content', element: <EducationalContentPage /> },
  { path: '/faq', element: <FAQPage /> },
  { path: '/blog', element: <BlogPage /> },
  // Company pages
  { path: '/about-us', element: <AboutUsPage /> },
  { path: '/our-mission', element: <OurMissionPage /> },
  { path: '/team', element: <TeamPage /> },
  { path: '/careers', element: <CareersPage /> },
  { path: '/press', element: <PressPage /> },
  { path: '/partners', element: <PartnersPage /> },
  // Support pages
  // Legal pages
  { path: '/privacy-policy', element: <PrivacyPolicyPage /> },
  { path: '/terms-of-service', element: <TermsOfServicePage /> },
  { path: '/accessibility', element: <AccessibilityPage /> },
  { path: '/sitemap', element: <SitemapPage /> },
  // Fix footer links - connect to ACTUAL existing pages
  { path: '/status', element: <StatusPage /> }, // Footer expects /status
  { path: '/help', element: <HelpPage /> }, // Footer expects /help
  { path: '/chat', element: <LiveChatPage /> }, // Footer expects /chat
  { path: '/bug-report', element: <BugReportPage /> }, // Footer expects /bug-report
  { path: '/feature-request', element: <FeatureRequestPage /> }, // Footer expects /feature-request
  { path: '/partners', element: <PartnersPage /> }, // Footer expects /partners
  { path: '/press', element: <PressPage /> }, // Footer expects /press
  { path: '/careers', element: <CareersPage /> }, // Footer expects /careers
  { path: '/team', element: <TeamPage /> }, // Footer expects /team
  { path: '/mission', element: <OurMissionPage /> }, // Footer expects /mission
  { path: '/about', element: <About /> }, // Footer expects /about
  { path: '/rights', element: <RightsPage /> }, // Footer expects /rights
  { path: '/glossary', element: <GlossaryPage /> }, // Footer expects /glossary
  { path: '/faq', element: <FAQPage /> }, // Footer expects /faq
  { path: '/blog', element: <BlogPage /> }, // Footer expects /blog
  { path: '/scan-document', element: <DocumentScanPage /> },
  { path: '/documents', element: <DocumentsPage /> },
  { path: '*', element: <Navigate to="/not-found" replace /> },
];

export default routes; 