from django.urls import path
from . import views

urlpatterns = [
    # --- Public Side ---
    # http://127.0.0.1:8000/menu/
    path('', views.menu_view, name='menu'),

    # http://127.0.0.1:8000/menu/favorites/
    path('favorites/', views.favorites_view, name='favorites'),

    # --- Staff / Admin Side ---
    # Inventory Management
    # http://127.0.0.1:8000/menu/staff/inventory/
    path('staff/inventory/', views.manage_inventory_view, name='inventory'),

    # Add Item
    # http://127.0.0.1:8000/menu/staff/inventory/add/
    path('staff/inventory/add/', views.add_item, name='add_item'),

    # Edit Item
    # http://127.0.0.1:8000/menu/staff/item/edit/5/
    path('staff/item/edit/<int:item_id>/', views.edit_menu_item_view, name='edit_item'),

    # Category Management
    # http://127.0.0.1:8000/menu/staff/categories/
    path('staff/categories/', views.manage_categories_view, name='categories'),

    # Edit Category
    # http://127.0.0.1:8000/menu/staff/categories/edit/1/
    path('staff/categories/edit/<int:category_id>/', views.edit_category_view, name='edit_category'),
]