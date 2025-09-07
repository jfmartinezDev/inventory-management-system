import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { 
  Package, 
  DollarSign, 
  AlertTriangle, 
  TrendingUp,
  Plus,
  ArrowRight,
  ShoppingCart,
  BarChart3
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import productService from '../services/product.service';
import { formatCurrency } from '../lib/utils';
import { QUERY_KEYS } from '../config/constants';

export default function Dashboard() {
  // Fetch inventory statistics
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: [QUERY_KEYS.INVENTORY_VALUE],
    queryFn: productService.getInventoryValue,
  });
  
  // Fetch recent products
  const { data: products, isLoading: productsLoading } = useQuery({
    queryKey: [QUERY_KEYS.PRODUCTS, 'recent'],
    queryFn: () => productService.getProducts({ page: 1, size: 5 }),
  });
  
  // Fetch low stock products
  const { data: lowStock, isLoading: lowStockLoading } = useQuery({
    queryKey: [QUERY_KEYS.PRODUCTS, 'low-stock'],
    queryFn: () => productService.getLowStockProducts({ page: 1, size: 5 }),
  });
  
  const isLoading = statsLoading || productsLoading || lowStockLoading;
  
  return (
    <div className="space-y-6 animate-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            Overview of your inventory management system
          </p>
        </div>
        <Link to="/products/new">
          <Button variant="gradient">
            <Plus className="mr-2 h-4 w-4" />
            Add Product
          </Button>
        </Link>
      </div>
      
      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Products
            </CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? '...' : stats?.total_products || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Active inventory items
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Value
            </CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? '...' : formatCurrency(stats?.total_value || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Current inventory value
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Low Stock Items
            </CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? '...' : stats?.low_stock_count || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              Items below minimum stock
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Avg. Product Value
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading 
                ? '...' 
                : formatCurrency(
                    stats?.total_products > 0 
                      ? stats.total_value / stats.total_products 
                      : 0
                  )
              }
            </div>
            <p className="text-xs text-muted-foreground">
              Per product average
            </p>
          </CardContent>
        </Card>
      </div>
      
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Products */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Recent Products</CardTitle>
              <CardDescription>
                Latest additions to inventory
              </CardDescription>
            </div>
            <ShoppingCart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="text-center py-4">Loading...</div>
            ) : products?.items?.length > 0 ? (
              <div className="space-y-4">
                {products.items.map((product) => (
                  <div 
                    key={product.id} 
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent transition-colors"
                  >
                    <div className="flex-1">
                      <h4 className="font-medium">{product.name}</h4>
                      <p className="text-sm text-muted-foreground">
                        SKU: {product.sku} | Stock: {product.quantity}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold">{formatCurrency(product.price)}</p>
                      <Link 
                        to={`/products/${product.id}`}
                        className="text-sm text-primary hover:underline"
                      >
                        View
                      </Link>
                    </div>
                  </div>
                ))}
                <Link to="/products" className="block">
                  <Button variant="outline" className="w-full">
                    View All Products
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="text-center py-8">
                <Package className="mx-auto h-12 w-12 text-muted-foreground mb-2" />
                <p className="text-muted-foreground mb-4">No products yet</p>
                <Link to="/products/new">
                  <Button variant="outline">Add First Product</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
        
        {/* Low Stock Alert */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Low Stock Alert</CardTitle>
              <CardDescription>
                Products that need restocking
              </CardDescription>
            </div>
            <AlertTriangle className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="text-center py-4">Loading...</div>
            ) : lowStock?.length > 0 ? (
              <div className="space-y-4">
                {lowStock.map((product) => (
                  <div 
                    key={product.id} 
                    className="flex items-center justify-between p-3 rounded-lg border border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20"
                  >
                    <div className="flex-1">
                      <h4 className="font-medium">{product.name}</h4>
                      <p className="text-sm text-muted-foreground">
                        Current: {product.quantity} | Min: {product.min_stock}
                      </p>
                    </div>
                    <Link 
                      to={`/products/${product.id}/edit`}
                      className="text-sm font-medium text-yellow-600 hover:underline"
                    >
                      Restock
                    </Link>
                  </div>
                ))}
                <Link to="/products?low_stock=true" className="block">
                  <Button variant="outline" className="w-full">
                    View All Low Stock Items
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="text-center py-8">
                <BarChart3 className="mx-auto h-12 w-12 text-muted-foreground mb-2" />
                <p className="text-muted-foreground">All products well stocked</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}