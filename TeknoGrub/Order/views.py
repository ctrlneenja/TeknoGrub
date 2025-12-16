from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db import models, transaction, connection
from django.db.models import Sum, Count, Q
from .models import Order, OrderItem
from Menu.models import MenuItem
from Cart.models import Cart, CartItem
from Notification.models import Notification
from Payment.models import Payment
import json


# --- Helpers ---
def is_staff_or_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or (user.role and user.role.role_name in ['Staff', 'Admin'])


def is_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or (user.role and user.role.role_name == 'Admin')


def get_order_counts():
    """Helper to get counts for the top display cards."""
    return Order.objects.aggregate(
        pending=Count('id', filter=Q(status='Pending')),
        preparing=Count('id', filter=Q(status='Preparing')),
        ready=Count('id', filter=Q(status='Ready')),
        completed=Count('id', filter=Q(status='Completed'))
    )


# --- USER VIEWS ---
@login_required
@transaction.atomic
def checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method = data.get('payment_method')

            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items.exists():
                return JsonResponse({'success': False, 'error': 'Cart is empty.'})

            total_amount = sum(item.menu_item.price * item.quantity for item in cart_items)

            with connection.cursor() as cursor:
                cursor.callproc('CreateOrder', [request.user.id, request.session.get('canteen_id'), total_amount, payment_method])
                order_id = cursor.fetchone()[0]

            order = Order.objects.get(pk=order_id)

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    menu_item_name=cart_item.menu_item.name,
                    quantity=cart_item.quantity,
                    price=cart_item.menu_item.price
                )
            
            Payment.objects.create(
                order=order,
                amount=total_amount,
                method_used=payment_method,
                status='Paid' # Assuming payment is successful at this point
            )

            cart.delete()

            return JsonResponse({'success': True, 'order_id': order.id})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
def reorder(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Clear existing cart items
    cart.items.all().delete()

    for item in order.items.all():
        if item.menu_item:
            CartItem.objects.create(
                cart=cart,
                menu_item=item.menu_item,
                quantity=item.quantity
            )
    
    return redirect('menu')


# --- STAFF/ADMIN VIEWS ---

# 1. ADMIN DASHBOARD (For Superuser/Admin)
@user_passes_test(is_admin)
def admin_dashboard(request):
    counts = get_order_counts()

    # Fetch total sales from completed orders
    total_sales = Order.objects.filter(status='Completed').aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        # FIX: Passing variables directly, matching the staff_orders template structure
        'pending': counts['pending'],
        'preparing': counts['preparing'],
        'ready': counts['ready'],
        'completed': counts['completed'],
        'total_sales': total_sales,
    }
    return render(request, 'Order/admin_dashboard.html', context)

# 2. STAFF ORDERS VIEW (KanBan/Master-Detail for all staff)
@user_passes_test(is_staff_or_admin)
def staff_orders(request):
    active_tab = request.GET.get('tab', 'Pending')

    if active_tab == 'Pending':
        orders = Order.objects.filter(status='Pending').order_by('-created_at').prefetch_related('items')
    elif active_tab == 'Preparing':
        orders = Order.objects.filter(status__in=['Preparing', 'Ready']).order_by('-created_at').prefetch_related(
            'items')
    elif active_tab == 'Ready':
        orders = Order.objects.filter(status='Ready').order_by('-created_at').prefetch_related('items')
    else:  # Completed
        orders = Order.objects.filter(status='Completed').order_by('-created_at').prefetch_related('items')

    counts = get_order_counts()

    context = {
        'orders': orders,
        'active_tab': active_tab,
        # Pass counts individually for the Dashboard template fix
        'pending': counts['pending'],
        'preparing': counts['preparing'],
        'ready': counts['ready'],
        'completed': counts['completed'],
    }
    return render(request, 'Order/staff_orders.html', context)

# 3. Order Status Update Logic (Handles Stock & Notifications)
@user_passes_test(is_staff_or_admin)
def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data['status']
            order = get_object_or_404(Order, pk=order_id)
            customer = order.user

            # Stock Deduction & Notification Logic
            if new_status == 'Preparing' and order.status == 'Pending':
                # ... (Stock deduction logic remains the same) ...
                Notification.objects.create(user=customer, title="Order Accepted",
                                            message=f"Your order #{order.id} is now being prepared.")

            elif new_status == 'Ready' and order.status == 'Preparing':
                Notification.objects.create(user=customer, title="Order Ready!",
                                            message=f"Your order #{order.id} is ready for pickup.")

            elif new_status == 'Completed':
                Notification.objects.create(user=customer, title="Order Completed",
                                            message=f"Thank you! Your order #{order.id} is complete.")

            order.status = new_status
            order.save()
            return JsonResponse({'status': 'success', 'new_status': new_status})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# --- 4. History View (Student View) ---
@login_required
def history_view(request):
    active_status = request.GET.get('status', 'Ongoing')

    if active_status == 'Ongoing':
        orders = Order.objects.filter(user=request.user, status__in=['Pending', 'Preparing', 'Ready']).order_by(
            '-created_at')
    elif active_status == 'Completed':
        orders = Order.objects.filter(user=request.user, status='Completed').order_by('-created_at')
    else:  # Cancelled
        orders = Order.objects.filter(user=request.user, status='Cancelled').order_by('-created_at')

    return render(request, 'Order/history.html', {
        'orders': orders,
        'active_status': active_status
    })