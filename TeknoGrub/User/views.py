from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Users, Role
from Order.models import Order
from Menu.models import Favorite


def get_user_role(user):
    """Safely retrieves the role name for redirection logic."""
    if user.is_superuser:
        return 'Admin'
    return user.role.role_name if user.role else 'Student'


def login_view(request):
    if request.user.is_authenticated:
        role = get_user_role(request.user)

        if role == 'Admin' and request.user.is_superuser:
            return redirect('admin_dashboard')
        if role == 'Staff':
            return redirect('staff_orders')

        return redirect('menu')

    if request.method == 'POST':
        login_identifier = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=login_identifier, password=password)

        if user is not None:
            login(request, user)
            role = get_user_role(user)
            if role == 'Admin':
                return redirect('admin_dashboard')
            if role == 'Staff':
                return redirect('staff_orders')
            return redirect('menu')
        else:
            return render(request, 'User/login.html', {'error': 'Invalid ID Number or Password.'})

    return render(request, 'User/login.html')


# --- 2. Signup View ---
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        school_email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([first_name, last_name, id_number, school_email, password]):
            return render(request, 'User/signup.html', {'error': 'All fields are required.'})

        try:
            student_role = Role.objects.get(role_name='Student')

            user = Users.objects.create_user(
                id_number=id_number,
                password=password,
                email=school_email,
                first_name=first_name,
                last_name=last_name,
                school_email=school_email,
                role=student_role
            )

            return redirect('login')

        except Role.DoesNotExist:
            return render(request, 'User/signup.html', {'error': 'System error: Student role not found.'})
        except IntegrityError:
            return render(request, 'User/signup.html', {'error': 'Account already exists for this ID or Email.'})
        except Exception as e:
            return render(request, 'User/signup.html', {'error': f'An unexpected error occurred: {e}'})

    return render(request, 'User/signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def settings_view(request):
    orders_count = Order.objects.filter(user=request.user).count()
    fav_count = Favorite.objects.filter(user=request.user).count()

    return render(request, 'User/settings.html', {
        'orders_count': orders_count,
        'fav_count': fav_count
    })


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            return redirect('settings')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'User/password_change.html', {'form': form})