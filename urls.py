from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.favorites_view, name='favorites'),
    path('', views.menu_view, name='menu'),
    path('inventory', views.inventory_view, name='inventory'),
    path('categories', views.categories_view, name='categories'),
    path('edit_categories', views.edit_categories_view, name='edit_categories'),
]

