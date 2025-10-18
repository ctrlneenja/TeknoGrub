from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

# @login_required
def order_history_view(request):
    completed_orders = []
    ongoing_orders = []
    cancelled_orders = []

    if request.user.is_authenticated:
        all_orders = Order.objects.filter(
            user=request.user
        ).select_related(
            'cart', 'cart__canteen'
        ).prefetch_related(
            'items', 'items__menu_item'
        ).order_by('-order_time')

        completed_orders = all_orders.filter(status='Completed')
        ongoing_orders = all_orders.filter(status='Ongoing')
        cancelled_orders = all_orders.filter(status='Cancelled')

    context = {
        'completed_orders': completed_orders,
        'ongoing_orders': ongoing_orders,
        'cancelled_orders': cancelled_orders,
    }
    return render(request, 'order/history.html', context)