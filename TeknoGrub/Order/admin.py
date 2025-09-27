from django.contrib import admin
from .models import Cart, CartItem, CartItemAddOn, Order, OrderItem, OrderItemAddOn, Payment, Staff

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartItemAddOn)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemAddOn)
admin.site.register(Payment)
admin.site.register(Staff)


