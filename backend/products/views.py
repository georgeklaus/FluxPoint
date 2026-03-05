from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from .models import Category, Product, ProductReview
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductReviewSerializer
)


class CategoryListView(generics.ListAPIView):
    """List all active categories"""
    queryset = Category.objects.filter(is_active=True, parent=None)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    """Get category with its products"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ProductListView(generics.ListAPIView):
    """List products with filtering"""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter featured
        if self.request.query_params.get('featured') == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Filter on sale
        if self.request.query_params.get('on_sale') == 'true':
            queryset = queryset.filter(sale_price__isnull=False)
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """Get single product details"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class FeaturedProductsView(generics.ListAPIView):
    """Get featured products"""
    queryset = Product.objects.filter(is_active=True, is_featured=True)[:8]
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductReviewListCreateView(generics.ListCreateAPIView):
    """List and create product reviews"""
    serializer_class = ProductReviewSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        return ProductReview.objects.filter(
            product__slug=self.kwargs['product_slug'],
            is_approved=True
        )
    
    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs['product_slug'])
        serializer.save(user=self.request.user, product=product)
