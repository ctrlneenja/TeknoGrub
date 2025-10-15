from django.contrib import admin
from .models import Cart, CartItem, CartItemAddOn

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
# admin.site.register(CartItemAddOn)

