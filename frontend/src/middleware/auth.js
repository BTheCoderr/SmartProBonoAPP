/**
 * Authentication middleware for protecting routes
 * This is a client-side authentication check that can be used in components
 */

import { getCurrentUser } from '../lib/supabase/auth';

/**
 * Check if user is authenticated and redirect if not
 * @param {string} redirectTo - Path to redirect to if not authenticated
 * @returns {Promise<boolean>} - True if authenticated, false if redirected
 */
export async function requireAuth(redirectTo = '/login') {
  try {
    const user = await getCurrentUser();
    if (!user) {
      // Redirect to login page
      window.location.href = redirectTo;
      return false;
    }
    return true;
  } catch (error) {
    console.error('Auth check failed:', error);
    window.location.href = redirectTo;
    return false;
  }
}

/**
 * Check if user is authenticated without redirecting
 * @returns {Promise<boolean>} - True if authenticated
 */
export async function isAuthenticated() {
  try {
    const user = await getCurrentUser();
    return !!user;
  } catch (error) {
    console.error('Auth check failed:', error);
    return false;
  }
}

/**
 * Get current user or redirect to login
 * @param {string} redirectTo - Path to redirect to if not authenticated
 * @returns {Promise<Object|null>} - User object or null if redirected
 */
export async function getUserOrRedirect(redirectTo = '/login') {
  try {
    const user = await getCurrentUser();
    if (!user) {
      window.location.href = redirectTo;
      return null;
    }
    return user;
  } catch (error) {
    console.error('Auth check failed:', error);
    window.location.href = redirectTo;
    return null;
  }
}

/**
 * Protected route wrapper component
 * This can be used to wrap components that require authentication
 */
export function withAuth(WrappedComponent, redirectTo = '/login') {
  return function ProtectedComponent(props) {
    const [isAuth, setIsAuth] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
      const checkAuth = async () => {
        const authenticated = await isAuthenticated();
        setIsAuth(authenticated);
        setLoading(false);
        
        if (!authenticated) {
          window.location.href = redirectTo;
        }
      };

      checkAuth();
    }, [redirectTo]);

    if (loading) {
      return (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh' 
        }}>
          <div>Loading...</div>
        </div>
      );
    }

    if (!isAuth) {
      return null; // Will redirect
    }

    return <WrappedComponent {...props} />;
  };
}
