from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BlogPost, BlogCategory, BlogTag, BlogComment
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer,
    BlogCategorySerializer, BlogTagSerializer, BlogCommentSerializer
)


class BlogPostListView(generics.ListAPIView):
    """List published blog posts"""
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Filter by post type
        post_type = self.request.query_params.get('type')
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        
        # Featured only
        if self.request.query_params.get('featured') == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class BlogPostDetailView(generics.RetrieveAPIView):
    """Get single blog post"""
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogCategoryListView(generics.ListAPIView):
    """List blog categories"""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class BlogTagListView(generics.ListAPIView):
    """List blog tags"""
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class BlogCommentListCreateView(generics.ListCreateAPIView):
    """List and create blog comments"""
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return BlogComment.objects.filter(
            post__slug=self.kwargs['post_slug'],
            is_approved=True,
            parent=None
        )
    
    def perform_create(self, serializer):
        post = BlogPost.objects.get(slug=self.kwargs['post_slug'])
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(post=post, user=user)


class FeaturedBlogPostsView(generics.ListAPIView):
    """Get featured blog posts"""
    queryset = BlogPost.objects.filter(is_published=True, is_featured=True)[:4]
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
