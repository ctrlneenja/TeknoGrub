from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Category, Inventory, Favorite


# STUDENT / PUBLIC VIEWS
def menu_view(request):
    categories = Category.objects.all()
    active_category_name = request.GET.get('category', 'Dish')  # default 'Dish'

    # find category object, if it exists
    try:
        active_category = Category.objects.get(category_name=active_category_name)
        menu_items = MenuItem.objects.filter(category=active_category, is_available=True)
    except Category.DoesNotExist:
        # Fallback: show all or empty if category not found
        menu_items = MenuItem.objects.filter(is_available=True)

    return render(request, 'menu.html')

def favorites_view(request):
    return render(request, 'favorites.html')

# ADMIN / STAFF VIEWS
def manage_inventory_view(request):

    # Use select_related to get the associated Item name in one query
    inventory_list = Inventory.objects.select_related('item').all()

    context = {
        'inventory_list': inventory_list
    }
    return render(request, 'inventory.html', context)


def manage_categories_view(request):
    categories = Category.objects.all()
    # Count items in each category for the dashboard
    for cat in categories:
        cat.item_count = MenuItem.objects.filter(category=cat).count()

    return render(request, 'categories.html', {'categories': categories})


def edit_category_view(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)

    # Items currently in this category
    current_items = MenuItem.objects.filter(category=category)

    # Items NOT in this category (for the 'Assign More Items' list)
    other_items = MenuItem.objects.exclude(category=category)

    context = {
        'category': category,
        'current_items': current_items,
        'other_items': other_items,
    }
    return render(request, 'edit_category.html', context)


def add_item(request):
    return render(request, 'edit_item.html')


def edit_menu_item_view(request, item_id):
    #mock
    item = {
        'id': item_id,
        'name': 'Sample Item',
        'price': 0.00,
        'description': '',
    }
    return render(request, 'edit_item.html', {'item': item})