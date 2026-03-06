from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.WishlistView.as_view(), name='wishlist'),
    path('add/', views.AddToWishlistView.as_view(), name='add'),
    path('remove/<int:product_id>/', views.RemoveFromWishlistView.as_view(), name='remove'),
    path('clear/', views.ClearWishlistView.as_view(), name='clear'),
    path('check/<int:product_id>/', views.CheckWishlistView.as_view(), name='check'),
]
