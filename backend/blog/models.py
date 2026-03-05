from django.db import models
from django.conf import settings
from django.utils.text import slugify


class BlogCategory(models.Model):
    """Blog post category"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogTag(models.Model):
    """Blog post tags"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Blog post model"""
    POST_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('gallery', 'Gallery'),
        ('quote', 'Quote'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    
    post_type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default='standard'
    )
    
    # Content
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    
    # For different post types
    video_url = models.URLField(blank=True)  # For video posts
    audio_url = models.URLField(blank=True)  # For audio posts
    quote_text = models.TextField(blank=True)  # For quote posts
    quote_author = models.CharField(max_length=200, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Meta
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    """Blog comments"""
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField(max_length=200)  # For anonymous comments
    email = models.EmailField()  # For anonymous comments
    content = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='replies'
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
