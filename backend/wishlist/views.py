from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, AddToWishlistSerializer
from products.models import Product


class WishlistView(APIView):
    """Get current user's wishlist"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)


class AddToWishlistView(APIView):
    """Add item to wishlist"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_id = serializer.validated_data['product_id']
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )
        
        return Response({
            'message': 'Added to wishlist',
            'wishlist': WishlistSerializer(wishlist).data
        })


class RemoveFromWishlistView(APIView):
    """Remove item from wishlist"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, product_id):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        WishlistItem.objects.filter(
            wishlist=wishlist, product_id=product_id
        ).delete()
        
        return Response({
            'message': 'Removed from wishlist',
            'wishlist': WishlistSerializer(wishlist).data
        })


class ClearWishlistView(APIView):
    """Clear all items from wishlist"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.all().delete()
        
        return Response({
            'message': 'Wishlist cleared',
            'wishlist': WishlistSerializer(wishlist).data
        })


class CheckWishlistView(APIView):
    """Check if product is in wishlist"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, product_id):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            in_wishlist = wishlist.items.filter(product_id=product_id).exists()
        except Wishlist.DoesNotExist:
            in_wishlist = False
        
        return Response({'in_wishlist': in_wishlist})
