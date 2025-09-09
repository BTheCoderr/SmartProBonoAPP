// PremiumRouteGuard - simplified for development

const PremiumRouteGuard = ({ children, isPremium = false }) => {
  // During development, always allow access without premium checks
  console.log('PremiumRouteGuard accessed - premium checks disabled for development');
  return children;
};

export default PremiumRouteGuard; 