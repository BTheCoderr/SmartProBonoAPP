import { supabase } from './client';

/**
 * Get the current authenticated user
 * @returns {Promise<Object|null>} - User object or null if not authenticated
 */
export async function getCurrentUser() {
  try {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) {
      console.error('Error getting user:', error);
      return null;
    }
    return user;
  } catch (error) {
    console.error('Error getting user:', error);
    return null;
  }
}

/**
 * Get the current authenticated user or throw an error
 * @returns {Promise<Object>} - User object
 * @throws {Error} - If user is not authenticated
 */
export async function getUserOrThrow() {
  const user = await getCurrentUser();
  if (!user) {
    throw new Error('Unauthorized - Please log in to continue');
  }
  return user;
}

/**
 * Check if user is authenticated
 * @returns {Promise<boolean>} - True if authenticated
 */
export async function isAuthenticated() {
  const user = await getCurrentUser();
  return !!user;
}

/**
 * Sign out the current user
 * @returns {Promise<void>}
 */
export async function signOut() {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error('Error signing out:', error);
      throw error;
    }
  } catch (error) {
    console.error('Error signing out:', error);
    throw error;
  }
}

/**
 * Get the current session
 * @returns {Promise<Object|null>} - Session object or null
 */
export async function getCurrentSession() {
  try {
    const { data: { session }, error } = await supabase.auth.getSession();
    if (error) {
      console.error('Error getting session:', error);
      return null;
    }
    return session;
  } catch (error) {
    console.error('Error getting session:', error);
    return null;
  }
}
