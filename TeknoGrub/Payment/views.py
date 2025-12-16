from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserPaymentMethod


@login_required
def add_payment_method(request):
    if request.method == "POST":
        method_type = request.POST.get('method_type')

        if request.POST.get('is_default') == 'true':
            UserPaymentMethod.objects.filter(user=request.user).update(is_default=False)

        if method_type == 'GCash':
            gcash_number = request.POST.get('gcash_number')
            if gcash_number:
                UserPaymentMethod.objects.create(
                    user=request.user,
                    method_type='GCash',
                    account_number=gcash_number,
                    is_default=True
                )

        elif method_type == 'Card':
            full_card = request.POST.get('card_number', '')
            expiry = request.POST.get('expiry')
            if full_card and expiry:
                UserPaymentMethod.objects.create(
                    user=request.user,
                    method_type='Card',
                    masked_card_number=full_card[-4:],
                    expiry_date=expiry,
                    is_default=True
                )

        return redirect('settings')

    return redirect('settings')

@login_required
def delete_payment_method(request, method_id):
    UserPaymentMethod.objects.filter(pk=method_id, user=request.user).delete()
    return redirect('settings')