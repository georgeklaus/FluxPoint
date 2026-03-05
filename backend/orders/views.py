from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderListSerializer, CreateOrderSerializer
from cart.models import Cart


class OrderListView(generics.ListAPIView):
    """List user's orders"""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """Get order details"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_object(self):
        return Order.objects.get(
            user=self.request.user,
            order_number=self.kwargs['order_number']
        )


class CreateOrderView(APIView):
    """Create new order from cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create order
        data = serializer.validated_data
        order = Order.objects.create(
            user=request.user,
            email=request.user.email,
            phone=data.get('phone', request.user.phone),
            
            # Shipping
            shipping_name=data['shipping_name'],
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            shipping_state=data['shipping_state'],
            shipping_zip=data['shipping_zip'],
            shipping_country=data.get('shipping_country', 'United States'),
            
            # Billing
            billing_name=data.get('billing_name', data['shipping_name']),
            billing_address=data.get('billing_address', data['shipping_address']),
            billing_city=data.get('billing_city', data['shipping_city']),
            billing_state=data.get('billing_state', data['shipping_state']),
            billing_zip=data.get('billing_zip', data['shipping_zip']),
            billing_country=data.get('billing_country', data.get('shipping_country', 'United States')),
            
            # Totals
            subtotal=cart.subtotal,
            shipping_cost=data.get('shipping_cost', 0),
            tax=data.get('tax', 0),
            total=cart.total + data.get('shipping_cost', 0) + data.get('tax', 0),
            
            payment_method=data.get('payment_method', ''),
            notes=data.get('notes', '')
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price
            )
            # Decrease stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.clear()
        
        return Response({
            'message': 'Order created successfully',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class CancelOrderView(APIView):
    """Cancel an order"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, order_number):
        try:
            order = Order.objects.get(
                user=request.user,
                order_number=order_number
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if order.status not in ['pending', 'processing']:
            return Response(
                {'error': 'Order cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        # Restore stock
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()
        
        return Response({
            'message': 'Order cancelled',
            'order': OrderSerializer(order).data
        })
