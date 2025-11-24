from django.shortcuts import render

# Create your views here.
def favorites_view(request):
    return render(request, "favorites.html")

def menu_view(request):
    return render(request, "menu.html")

def categories_view(request):
    return render(request, "categories.html")

def edit_categories_view(request):
    return render(request, "edit_category.html")

def inventory_view(request):
    return render(request, "inventory.html")