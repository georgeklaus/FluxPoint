from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('csrf/', views.CSRFTokenView.as_view(), name='csrf'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('check/', views.CheckAuthView.as_view(), name='check_auth'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('addresses/', views.AddressListCreateView.as_view(), name='address_list'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address_detail'),
]
