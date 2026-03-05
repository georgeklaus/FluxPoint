from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from products.models import Product


class CartMixin:
    """Mixin to get or create cart"""
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


class CartView(CartMixin, APIView):
    """Get current cart"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(CartMixin, APIView):
    """Add item to cart"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart = self.get_cart(request)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'message': 'Added to cart',
            'cart': CartSerializer(cart).data
        })


class UpdateCartItemView(CartMixin, APIView):
    """Update cart item quantity"""
    permission_classes = [permissions.AllowAny]
    
    def put(self, request, item_id):
        cart = self.get_cart(request)
        quantity = request.data.get('quantity', 1)
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if quantity <= 0:
            cart_item.delete()
            return Response({
                'message': 'Item removed',
                'cart': CartSerializer(cart).data
            })
        
        if cart_item.product.stock < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'message': 'Cart updated',
            'cart': CartSerializer(cart).data
        })


class RemoveFromCartView(CartMixin, APIView):
    """Remove item from cart"""
    permission_classes = [permissions.AllowAny]
    
    def delete(self, request, item_id):
        cart = self.get_cart(request)
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        
        return Response({
            'message': 'Item removed',
            'cart': CartSerializer(cart).data
        })


class ClearCartView(CartMixin, APIView):
    """Clear all items from cart"""
    permission_classes = [permissions.AllowAny]
    
    def delete(self, request):
        cart = self.get_cart(request)
        cart.clear()
        return Response({
            'message': 'Cart cleared',
            'cart': CartSerializer(cart).data
        })
