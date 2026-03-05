from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:product_slug>/reviews/', views.ProductReviewListCreateView.as_view(), name='product_reviews'),
]
