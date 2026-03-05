from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.middleware.csrf import get_token
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    ChangePasswordSerializer, AddressSerializer
)
from .models import Address

User = get_user_model()


class CSRFTokenView(APIView):
    """Get CSRF token for frontend"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({'csrfToken': get_token(request)})


class RegisterView(generics.CreateAPIView):
    """User registration"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """User login"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            })
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """User logout"""
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password changed successfully'})


class AddressListCreateView(generics.ListCreateAPIView):
    """List and create addresses"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, delete specific address"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class CheckAuthView(APIView):
    """Check if user is authenticated"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user': UserSerializer(request.user).data
            })
        return Response({'authenticated': False})
