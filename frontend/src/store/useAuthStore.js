import { create } from 'zustand';
import authService from '../services/auth.service';

/**
 * Global authentication state management
 */
const useAuthStore = create((set) => ({
  user: authService.getCurrentUser(),
  isAuthenticated: authService.isAuthenticated(),
  isLoading: false,
  error: null,
  
  /**
   * Login user
   * @param {Object} credentials - Login credentials
   * @returns {Promise<void>}
   */
  login: async (credentials) => {
    set({ isLoading: true, error: null });
    try {
      const { user } = await authService.login(credentials);
      set({ 
        user, 
        isAuthenticated: true, 
        isLoading: false,
        error: null 
      });
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error.response?.data?.detail || 'Login failed' 
      });
      throw error;
    }
  },
  
  /**
   * Register new user
   * @param {Object} userData - Registration data
   * @returns {Promise<void>}
   */
  register: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      await authService.register(userData);
      set({ isLoading: false, error: null });
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      });
      throw error;
    }
  },
  
  /**
   * Logout user
   */
  logout: () => {
    authService.logout();
    set({ 
      user: null, 
      isAuthenticated: false,
      error: null 
    });
  },
  
  /**
   * Update user profile
   * @param {Object} userData - Updated user data
   * @returns {Promise<void>}
   */
  updateProfile: async (userData) => {
    set({ isLoading: true, error: null });
    try {
      const updatedUser = await authService.updateProfile(userData);
      set({ 
        user: updatedUser, 
        isLoading: false,
        error: null 
      });
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error.response?.data?.detail || 'Update failed' 
      });
      throw error;
    }
  },
  
  /**
   * Clear error state
   */
  clearError: () => set({ error: null }),
}));

export default useAuthStore;