from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'product_sku', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'email', 'total', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'email', 'shipping_name']
    readonly_fields = ['order_number', 'subtotal', 'total', 'created_at']
    inlines = [OrderItemInline]
    list_editable = ['status', 'payment_status']
    
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'email', 'phone', 'status', 'payment_status', 'payment_method')}),
        ('Shipping', {'fields': ('shipping_name', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'shipping_country')}),
        ('Billing', {'fields': ('billing_name', 'billing_address', 'billing_city', 'billing_state', 'billing_zip', 'billing_country')}),
        ('Totals', {'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total')}),
        ('Notes', {'fields': ('notes',)}),
    )
