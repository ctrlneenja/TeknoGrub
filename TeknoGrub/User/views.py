from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def settings(request):
    return render(request, 'User/settings.html')
