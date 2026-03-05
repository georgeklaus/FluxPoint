from django.contrib import admin
from .models import BlogCategory, BlogTag, BlogPost, BlogComment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'post_type', 'is_published', 'is_featured', 'views', 'created_at']
    list_filter = ['is_published', 'is_featured', 'post_type', 'category', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_featured']
    filter_horizontal = ['tags']
    
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'category', 'tags')}),
        ('Content', {'fields': ('post_type', 'excerpt', 'content', 'featured_image')}),
        ('Media', {'fields': ('video_url', 'audio_url', 'quote_text', 'quote_author')}),
        ('Status', {'fields': ('is_published', 'is_featured', 'published_at')}),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'content']
