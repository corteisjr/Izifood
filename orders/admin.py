from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'telephone', 'address', 'postal_code', 'city', 'created', 'updated', 'status', 'transport', 'transport_price', 'note']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]
    
    
