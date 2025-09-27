from django.contrib import admin
from .models import Category, PromoName, PromoItem, PromoCategory, PromoRedemption

# Register your models here.
admin.site.register(Category)
admin.site.register(PromoName)
admin.site.register(PromoItem)
admin.site.register(PromoCategory)
admin.site.register(PromoRedemption)

