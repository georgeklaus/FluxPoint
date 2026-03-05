from rest_framework import serializers
from .models import BlogPost, BlogCategory, BlogTag, BlogComment


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for blog categories"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'post_count']
    
    def get_post_count(self, obj):
        return obj.posts.filter(is_published=True).count()


class BlogTagSerializer(serializers.ModelSerializer):
    """Serializer for blog tags"""
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug']


class BlogCommentSerializer(serializers.ModelSerializer):
    """Serializer for blog comments"""
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogComment
        fields = ['id', 'name', 'email', 'content', 'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'replies', 'created_at']
    
    def get_replies(self, obj):
        replies = obj.replies.filter(is_approved=True)
        return BlogCommentSerializer(replies, many=True).data


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for blog post list"""
    author_name = serializers.SerializerMethodField()
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author_name', 'category', 'tags',
            'post_type', 'excerpt', 'featured_image', 'is_featured',
            'views', 'comment_count', 'created_at'
        ]
    
    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog post detail"""
    author_name = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author_name', 'author_avatar',
            'category', 'tags', 'post_type', 'excerpt', 'content',
            'featured_image', 'video_url', 'audio_url',
            'quote_text', 'quote_author', 'is_featured',
            'views', 'comment_count', 'created_at', 'published_at'
        ]
    
    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    
    def get_author_avatar(self, obj):
        if obj.author.avatar:
            return obj.author.avatar.url
        return None
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
