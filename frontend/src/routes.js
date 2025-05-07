import React from 'react';
import { Navigate } from 'react-router-dom';

// Lazy load components
const Home = React.lazy(() => import('./pages/Home'));
const About = React.lazy(() => import('./pages/About'));
const Login = React.lazy(() => import('./pages/LoginPage'));
const Register = React.lazy(() => import('./pages/RegisterPage'));
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const BetaLanding = React.lazy(() => import('./pages/BetaLandingPage'));
const LegalChat = React.lazy(() => import('./pages/LegalChat'));
const Documents = React.lazy(() => import('./pages/Documents'));
const ExpertHelp = React.lazy(() => import('./pages/ExpertHelp'));
const BetaConfirm = React.lazy(() => import('./pages/BetaConfirm'));
const BusinessModel = React.lazy(() => import('./pages/BusinessModel'));

const routes = [
  {
    path: '/',
    element: <BetaLanding />,
  },
  {
    path: '/home',
    element: <Home />,
  },
  {
    path: '/about',
    element: <About />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/register',
    element: <Register />,
  },
  {
    path: '/dashboard',
    element: <Dashboard />,
  },
  {
    path: '/legal-chat',
    element: <LegalChat />,
  },
  {
    path: '/documents',
    element: <Documents />,
  },
  {
    path: '/expert-help',
    element: <ExpertHelp />,
  },
  {
    path: '/business-model',
    element: <BusinessModel />,
  },
  {
    path: '/beta/confirm/:token',
    element: <BetaConfirm />,
  },
  {
    path: '*',
    element: <Navigate to="/" replace />,
  },
];

export default routes; 