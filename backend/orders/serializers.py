from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product_name', 'product_sku', 'quantity',
            'unit_price', 'total_price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order details"""
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'email', 'phone',
            'shipping_name', 'shipping_address', 'shipping_city',
            'shipping_state', 'shipping_zip', 'shipping_country',
            'billing_name', 'billing_address', 'billing_city',
            'billing_state', 'billing_zip', 'billing_country',
            'subtotal', 'shipping_cost', 'tax', 'discount', 'total',
            'status', 'payment_status', 'payment_method',
            'notes', 'items', 'created_at', 'updated_at'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order list"""
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total', 'status',
            'payment_status', 'item_count', 'created_at'
        ]
    
    def get_item_count(self, obj):
        return obj.items.count()


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders"""
    # Shipping
    shipping_name = serializers.CharField(max_length=200)
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=100)
    shipping_zip = serializers.CharField(max_length=20)
    shipping_country = serializers.CharField(max_length=100, default='United States')
    
    # Billing (optional - defaults to shipping)
    billing_name = serializers.CharField(max_length=200, required=False)
    billing_address = serializers.CharField(required=False)
    billing_city = serializers.CharField(max_length=100, required=False)
    billing_state = serializers.CharField(max_length=100, required=False)
    billing_zip = serializers.CharField(max_length=20, required=False)
    billing_country = serializers.CharField(max_length=100, required=False)
    
    # Contact
    phone = serializers.CharField(max_length=20, required=False)
    
    # Payment
    payment_method = serializers.CharField(max_length=50, required=False)
    
    # Other
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = serializers.CharField(required=False, allow_blank=True)
