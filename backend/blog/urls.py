from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='post_list'),
    path('featured/', views.FeaturedBlogPostsView.as_view(), name='featured'),
    path('categories/', views.BlogCategoryListView.as_view(), name='category_list'),
    path('tags/', views.BlogTagListView.as_view(), name='tag_list'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('<slug:post_slug>/comments/', views.BlogCommentListCreateView.as_view(), name='comments'),
]
