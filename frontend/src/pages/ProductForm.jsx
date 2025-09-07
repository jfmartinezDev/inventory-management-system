import React, { useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { toast } from 'react-hot-toast';
import { ArrowLeft, Save, Package } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import productService from '../services/product.service';
import { QUERY_KEYS } from '../config/constants';

// Validation schema
const productSchema = z.object({
  name: z.string().min(1, 'Product name is required').max(200),
  description: z.string().optional(),
  sku: z.string().min(1, 'SKU is required').max(100),
  price: z.number().positive('Price must be greater than 0'),
  quantity: z.number().int().min(0, 'Quantity cannot be negative'),
  min_stock: z.number().int().min(0, 'Minimum stock cannot be negative'),
  category: z.string().optional(),
  image_url: z.string().url().optional().or(z.literal('')),
});

export default function ProductForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = !!id;
  
  // Fetch product if editing
  const { data: product, isLoading: productLoading } = useQuery({
    queryKey: [QUERY_KEYS.PRODUCT, id],
    queryFn: () => productService.getProduct(id),
    enabled: isEdit,
  });
  
  // Fetch categories for dropdown
  const { data: categories } = useQuery({
    queryKey: [QUERY_KEYS.CATEGORIES],
    queryFn: productService.getCategories,
  });
  
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    setValue,
  } = useForm({
    resolver: zodResolver(productSchema),
    defaultValues: {
      name: '',
      description: '',
      sku: '',
      price: 0,
      quantity: 0,
      min_stock: 0,
      category: '',
      image_url: '',
    },
  });
  
  // Update form when product data is loaded
  useEffect(() => {
    if (product) {
      reset({
        name: product.name,
        description: product.description || '',
        sku: product.sku,
        price: product.price,
        quantity: product.quantity,
        min_stock: product.min_stock,
        category: product.category || '',
        image_url: product.image_url || '',
      });
    }
  }, [product, reset]);
  
  // Create mutation
  const createMutation = useMutation({
    mutationFn: productService.createProduct,
    onSuccess: (data) => {
      queryClient.invalidateQueries([QUERY_KEYS.PRODUCTS]);
      toast.success('Product created successfully');
      navigate(`/products/${data.id}`);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create product');
    },
  });
  
  // Update mutation
  const updateMutation = useMutation({
    mutationFn: (data) => productService.updateProduct(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.PRODUCTS]);
      queryClient.invalidateQueries([QUERY_KEYS.PRODUCT, id]);
      toast.success('Product updated successfully');
      navigate(`/products/${id}`);
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update product');
    },
  });
  
  const onSubmit = async (data) => {
    // Convert price to number
    data.price = parseFloat(data.price);
    data.quantity = parseInt(data.quantity);
    data.min_stock = parseInt(data.min_stock);
    
    // Clean empty strings
    if (!data.description) delete data.description;
    if (!data.category) delete data.category;
    if (!data.image_url) delete data.image_url;
    
    if (isEdit) {
      updateMutation.mutate(data);
    } else {
      createMutation.mutate(data);
    }
  };
  
  if (isEdit && productLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to="/products">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold">
            {isEdit ? 'Edit Product' : 'New Product'}
          </h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update product information' : 'Add a new product to inventory'}
          </p>
        </div>
      </div>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid gap-6">
          {/* Basic Information */}
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>
                Enter the basic details of the product
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label htmlFor="name" className="text-sm font-medium">
                    Product Name <span className="text-red-500">*</span>
                  </label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="Enter product name"
                    {...register('name')}
                    className={errors.name ? 'border-red-500' : ''}
                  />
                  {errors.name && (
                    <p className="text-xs text-red-500">{errors.name.message}</p>
                  )}
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="sku" className="text-sm font-medium">
                    SKU <span className="text-red-500">*</span>
                  </label>
                  <Input
                    id="sku"
                    type="text"
                    placeholder="Enter unique SKU"
                    {...register('sku')}
                    className={errors.sku ? 'border-red-500' : ''}
                  />
                  {errors.sku && (
                    <p className="text-xs text-red-500">{errors.sku.message}</p>
                  )}
                </div>
              </div>
              
              <div className="space-y-2">
                <label htmlFor="description" className="text-sm font-medium">
                  Description
                </label>
                <textarea
                  id="description"
                  rows={3}
                  placeholder="Enter product description (optional)"
                  className="w-full px-3 py-2 border rounded-md bg-background"
                  {...register('description')}
                />
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label htmlFor="category" className="text-sm font-medium">
                    Category
                  </label>
                  <div className="relative">
                    <Input
                      id="category"
                      type="text"
                      placeholder="Enter or select category"
                      list="categories"
                      {...register('category')}
                    />
                    <datalist id="categories">
                      {categories?.map((cat) => (
                        <option key={cat} value={cat} />
                      ))}
                    </datalist>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="image_url" className="text-sm font-medium">
                    Image URL
                  </label>
                  <Input
                    id="image_url"
                    type="url"
                    placeholder="https://example.com/image.jpg"
                    {...register('image_url')}
                    className={errors.image_url ? 'border-red-500' : ''}
                  />
                  {errors.image_url && (
                    <p className="text-xs text-red-500">{errors.image_url.message}</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
          
          {/* Pricing and Inventory */}
          <Card>
            <CardHeader>
              <CardTitle>Pricing & Inventory</CardTitle>
              <CardDescription>
                Set pricing and stock levels
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label htmlFor="price" className="text-sm font-medium">
                    Price <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                      $
                    </span>
                    <Input
                      id="price"
                      type="number"
                      step="0.01"
                      placeholder="0.00"
                      className={`pl-8 ${errors.price ? 'border-red-500' : ''}`}
                      {...register('price', { valueAsNumber: true })}
                    />
                  </div>
                  {errors.price && (
                    <p className="text-xs text-red-500">{errors.price.message}</p>
                  )}
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="quantity" className="text-sm font-medium">
                    Current Stock <span className="text-red-500">*</span>
                  </label>
                  <Input
                    id="quantity"
                    type="number"
                    placeholder="0"
                    {...register('quantity', { valueAsNumber: true })}
                    className={errors.quantity ? 'border-red-500' : ''}
                  />
                  {errors.quantity && (
                    <p className="text-xs text-red-500">{errors.quantity.message}</p>
                  )}
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="min_stock" className="text-sm font-medium">
                    Minimum Stock
                  </label>
                  <Input
                    id="min_stock"
                    type="number"
                    placeholder="0"
                    {...register('min_stock', { valueAsNumber: true })}
                    className={errors.min_stock ? 'border-red-500' : ''}
                  />
                  {errors.min_stock && (
                    <p className="text-xs text-red-500">{errors.min_stock.message}</p>
                  )}
                  <p className="text-xs text-muted-foreground">
                    Alert when stock falls below this level
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          {/* Actions */}
          <div className="flex justify-end gap-4">
            <Link to="/products">
              <Button type="button" variant="outline">
                Cancel
              </Button>
            </Link>
            <Button 
              type="submit" 
              disabled={isSubmitting || createMutation.isLoading || updateMutation.isLoading}
              variant="gradient"
            >
              {isSubmitting || createMutation.isLoading || updateMutation.isLoading ? (
                <>
                  <span className="animate-spin mr-2">⏳</span>
                  {isEdit ? 'Updating...' : 'Creating...'}
                </>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  {isEdit ? 'Update Product' : 'Create Product'}
                </>
              )}
            </Button>
          </div>
        </div>
      </form>
    </div>
  );
}