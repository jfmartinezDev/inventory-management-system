import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { 
  ArrowLeft, 
  Edit, 
  Trash2, 
  Package, 
  DollarSign,
  Hash,
  Calendar,
  AlertTriangle,
  Plus,
  Minus
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import productService from '../services/product.service';
import { formatCurrency, formatDateTime } from '../lib/utils';
import { QUERY_KEYS } from '../config/constants';

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [stockAdjustment, setStockAdjustment] = useState('');
  
  // Fetch product details
  const { data: product, isLoading, error } = useQuery({
    queryKey: [QUERY_KEYS.PRODUCT, id],
    queryFn: () => productService.getProduct(id),
  });
  
  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: () => productService.deleteProduct(id),
    onSuccess: () => {
      toast.success('Product deleted successfully');
      navigate('/products');
    },
    onError: () => {
      toast.error('Failed to delete product');
    },
  });
  
  // Stock update mutation
  const stockMutation = useMutation({
    mutationFn: (quantity) => productService.updateStock(id, quantity),
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.PRODUCT, id]);
      toast.success('Stock updated successfully');
      setStockAdjustment('');
    },
    onError: () => {
      toast.error('Failed to update stock');
    },
  });
  
  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
      deleteMutation.mutate();
    }
  };
  
  const handleStockAdjustment = (type) => {
    const quantity = parseInt(stockAdjustment);
    if (isNaN(quantity) || quantity === 0) {
      toast.error('Please enter a valid quantity');
      return;
    }
    
    const adjustedQuantity = type === 'add' ? quantity : -quantity;
    stockMutation.mutate(adjustedQuantity);
  };
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  if (error || !product) {
    return (
      <div className="text-center py-12">
        <Package className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
        <h2 className="text-2xl font-semibold mb-2">Product Not Found</h2>
        <p className="text-muted-foreground mb-4">
          The product you're looking for doesn't exist or has been removed.
        </p>
        <Link to="/products">
          <Button>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Products
          </Button>
        </Link>
      </div>
    );
  }
  
  return (
    <div className="space-y-6 animate-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/products">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold">{product.name}</h1>
            <p className="text-muted-foreground">Product Details</p>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Link to={`/products/${id}/edit`}>
            <Button variant="outline">
              <Edit className="mr-2 h-4 w-4" />
              Edit
            </Button>
          </Link>
          <Button 
            variant="destructive"
            onClick={handleDelete}
            disabled={deleteMutation.isLoading}
          >
            <Trash2 className="mr-2 h-4 w-4" />
            Delete
          </Button>
        </div>
      </div>
      
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Product Image and Basic Info */}
          <Card>
            <CardContent className="p-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  {product.image_url ? (
                    <img 
                      src={product.image_url} 
                      alt={product.name}
                      className="w-full h-64 object-cover rounded-lg"
                    />
                  ) : (
                    <div className="w-full h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                      <Package className="h-20 w-20 text-gray-400" />
                    </div>
                  )}
                </div>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">SKU</label>
                    <div className="flex items-center gap-2 mt-1">
                      <Hash className="h-4 w-4 text-muted-foreground" />
                      <code className="text-lg font-mono bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded">
                        {product.sku}
                      </code>
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">Price</label>
                    <div className="flex items-center gap-2 mt-1">
                      <DollarSign className="h-4 w-4 text-muted-foreground" />
                      <span className="text-2xl font-bold">{formatCurrency(product.price)}</span>
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-muted-foreground">Category</label>
                    <div className="mt-1">
                      {product.category ? (
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                          {product.category}
                        </span>
                      ) : (
                        <span className="text-muted-foreground">Uncategorized</span>
                      )}
                    </div>
                  </div>
                  
                  {product.description && (
                    <div>
                      <label className="text-sm font-medium text-muted-foreground">Description</label>
                      <p className="mt-1 text-sm">{product.description}</p>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
          
          {/* Stock Management */}
          <Card>
            <CardHeader>
              <CardTitle>Stock Management</CardTitle>
              <CardDescription>Adjust product inventory levels</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-muted-foreground">Current Stock</p>
                    <p className="text-3xl font-bold mt-1">{product.quantity}</p>
                  </div>
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-muted-foreground">Min Stock</p>
                    <p className="text-3xl font-bold mt-1">{product.min_stock}</p>
                  </div>
                  <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm text-muted-foreground">Total Value</p>
                    <p className="text-2xl font-bold mt-1">{formatCurrency(product.total_value)}</p>
                  </div>
                </div>
                
                {product.is_low_stock && (
                  <div className="flex items-center gap-2 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                    <AlertTriangle className="h-5 w-5 text-yellow-600" />
                    <span className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                      Low stock alert! Current stock is below minimum level.
                    </span>
                  </div>
                )}
                
                <div className="flex gap-2">
                  <Input
                    type="number"
                    placeholder="Enter quantity"
                    value={stockAdjustment}
                    onChange={(e) => setStockAdjustment(e.target.value)}
                    className="flex-1"
                  />
                  <Button 
                    onClick={() => handleStockAdjustment('add')}
                    disabled={stockMutation.isLoading}
                    variant="outline"
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    Add Stock
                  </Button>
                  <Button 
                    onClick={() => handleStockAdjustment('remove')}
                    disabled={stockMutation.isLoading}
                    variant="outline"
                  >
                    <Minus className="mr-2 h-4 w-4" />
                    Remove Stock
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Sidebar */}
        <div className="space-y-6">
          {/* Metadata */}
          <Card>
            <CardHeader>
              <CardTitle>Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Product ID</label>
                <p className="text-sm font-mono">{product.id}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-muted-foreground">Created</label>
                <p className="text-sm flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formatDateTime(product.created_at)}
                </p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-muted-foreground">Last Updated</label>
                <p className="text-sm flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formatDateTime(product.updated_at)}
                </p>
              </div>
            </CardContent>
          </Card>
          
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Link to={`/products/${id}/edit`} className="block">
                <Button variant="outline" className="w-full justify-start">
                  <Edit className="mr-2 h-4 w-4" />
                  Edit Product
                </Button>
              </Link>
              <Button 
                variant="outline" 
                className="w-full justify-start"
                onClick={() => {
                  navigator.clipboard.writeText(product.sku);
                  toast.success('SKU copied to clipboard');
                }}
              >
                <Hash className="mr-2 h-4 w-4" />
                Copy SKU
              </Button>
              <Button 
                variant="outline" 
                className="w-full justify-start text-red-600 hover:text-red-700"
                onClick={handleDelete}
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete Product
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}