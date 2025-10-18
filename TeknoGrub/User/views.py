from django.shortcuts import render

def settings(request):
    return render(request, 'User/settings.html')

def login_view(request):
    return render(request, 'User/login.html')
