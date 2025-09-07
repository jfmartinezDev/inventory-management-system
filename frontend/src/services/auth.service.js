import api from './api';
import { STORAGE_KEYS } from '../config/constants';

/**
 * Authentication service for user login, registration, and token management
 */
class AuthService {
  /**
   * Login user with username and password
   * @param {Object} credentials - Login credentials
   * @param {string} credentials.username - Username or email
   * @param {string} credentials.password - Password
   * @returns {Promise<Object>} User data and token
   */
  async login(credentials) {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const { access_token } = response.data;
    
    // Store token
    localStorage.setItem(STORAGE_KEYS.TOKEN, access_token);
    
    // Get user data
    const userResponse = await api.get('/users/me');
    const userData = userResponse.data;
    
    // Store user data
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userData));
    
    return {
      token: access_token,
      user: userData,
    };
  }
  
  /**
   * Register new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Created user data
   */
  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  }
  
  /**
   * Logout user and clear stored data
   */
  logout() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  }
  
  /**
   * Get current user from storage
   * @returns {Object|null} User data or null
   */
  getCurrentUser() {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);
    return userStr ? JSON.parse(userStr) : null;
  }
  
  /**
   * Check if user is authenticated
   * @returns {boolean} Authentication status
   */
  isAuthenticated() {
    return !!localStorage.getItem(STORAGE_KEYS.TOKEN);
  }
  
  /**
   * Get current token
   * @returns {string|null} Token or null
   */
  getToken() {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
  }
  
  /**
   * Update current user profile
   * @param {Object} userData - Updated user data
   * @returns {Promise<Object>} Updated user data
   */
  async updateProfile(userData) {
    const response = await api.put('/users/me', userData);
    const updatedUser = response.data;
    
    // Update stored user data
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(updatedUser));
    
    return updatedUser;
  }
}

export default new AuthService();