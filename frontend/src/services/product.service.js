import api from './api';

/**
 * Product service for inventory management operations
 */
class ProductService {
  /**
   * Get paginated products list
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} Paginated products
   */
  async getProducts(params = {}) {
    const response = await api.get('/products', { params });
    return response.data;
  }
  
  /**
   * Get single product by ID
   * @param {number} id - Product ID
   * @returns {Promise<Object>} Product data
   */
  async getProduct(id) {
    const response = await api.get(`/products/${id}`);
    return response.data;
  }
  
  /**
   * Create new product
   * @param {Object} productData - Product data
   * @returns {Promise<Object>} Created product
   */
  async createProduct(productData) {
    const response = await api.post('/products', productData);
    return response.data;
  }
  
  /**
   * Update existing product
   * @param {number} id - Product ID
   * @param {Object} productData - Updated product data
   * @returns {Promise<Object>} Updated product
   */
  async updateProduct(id, productData) {
    const response = await api.put(`/products/${id}`, productData);
    return response.data;
  }
  
  /**
   * Delete product
   * @param {number} id - Product ID
   * @returns {Promise<void>}
   */
  async deleteProduct(id) {
    await api.delete(`/products/${id}`);
  }
  
  /**
   * Update product stock
   * @param {number} id - Product ID
   * @param {number} quantityChange - Quantity to add or subtract
   * @returns {Promise<Object>} Updated product
   */
  async updateStock(id, quantityChange) {
    const response = await api.patch(`/products/${id}/stock`, null, {
      params: { quantity_change: quantityChange }
    });
    return response.data;
  }
  
  /**
   * Search products
   * @param {string} query - Search query
   * @param {Object} params - Additional parameters
   * @returns {Promise<Object>} Search results
   */
  async searchProducts(query, params = {}) {
    const response = await api.get('/products', {
      params: { search: query, ...params }
    });
    return response.data;
  }
  
  /**
   * Get products by category
   * @param {string} category - Category name
   * @param {Object} params - Additional parameters
   * @returns {Promise<Object>} Products in category
   */
  async getProductsByCategory(category, params = {}) {
    const response = await api.get('/products', {
      params: { category, ...params }
    });
    return response.data;
  }
  
  /**
   * Get low stock products
   * @param {Object} params - Query parameters
   * @returns {Promise<Array>} Low stock products
   */
  async getLowStockProducts(params = {}) {
    const response = await api.get('/products/low-stock', { params });
    return response.data;
  }
  
  /**
   * Get all product categories
   * @returns {Promise<Array>} Categories list
   */
  async getCategories() {
    const response = await api.get('/products/categories');
    return response.data;
  }
  
  /**
   * Get inventory value statistics
   * @returns {Promise<Object>} Inventory statistics
   */
  async getInventoryValue() {
    const response = await api.get('/products/inventory-value');
    return response.data;
  }
}

export default new ProductService();
