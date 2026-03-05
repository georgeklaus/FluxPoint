"""
URL configuration for FluxPoint project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('accounts.urls', namespace='accounts')),
    path('api/products/', include('products.urls', namespace='products')),
    path('api/cart/', include('cart.urls', namespace='cart')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('api/wishlist/', include('wishlist.urls', namespace='wishlist')),
    path('api/blog/', include('blog.urls', namespace='blog')),
    
    # Frontend pages
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/sidebar/', views.ShopSidebarView.as_view(), name='shop_sidebar'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('my-account/', views.MyAccountView.as_view(), name='my_account'),
    path('sign-in/', views.SignInView.as_view(), name='sign_in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/grid/', views.BlogGridView.as_view(), name='blog_grid'),
    path('blog/<slug:slug>/', views.BlogDetailsView.as_view(), name='blog_details'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('coming-soon/', views.ComingSoonView.as_view(), name='coming_soon'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
