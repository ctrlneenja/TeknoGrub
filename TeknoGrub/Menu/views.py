from django.shortcuts import render

# Create your views here.
def favorites_view(request):
    return render(request, "favorites.html")

def menu_view(request):
    return render(request, "menu.html")