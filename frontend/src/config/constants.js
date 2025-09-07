/**
 * Application constants and configuration
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_VERSION = '/api/v1';
export const API_URL = `${API_BASE_URL}${API_VERSION}`;

// Storage Keys
export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  USER: 'user_data',
  THEME: 'app_theme',
};

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  PRODUCTS: '/products',
  PRODUCT_DETAIL: '/products/:id',
  PRODUCT_NEW: '/products/new',
  PRODUCT_EDIT: '/products/:id/edit',
  PROFILE: '/profile',
  SETTINGS: '/settings',
};

// Query Keys for React Query
export const QUERY_KEYS = {
  USER: 'user',
  USERS: 'users',
  PRODUCTS: 'products',
  PRODUCT: 'product',
  CATEGORIES: 'categories',
  INVENTORY_VALUE: 'inventory-value',
};

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_SIZE: 10,
  SIZE_OPTIONS: [10, 25, 50, 100],
};