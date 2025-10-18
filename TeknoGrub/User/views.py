from django.shortcuts import render

def settings_view(request):
    return render(request, 'User/settings.html')

def login_view(request):
    return render(request, 'User/login.html')

def signup_view(request):
    return render(request, 'User/signup.html')
