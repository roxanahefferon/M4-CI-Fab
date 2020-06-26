from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There are no items in your basket at the moment")
        return redirect(reverse('catalogue'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51GyHQQGxUCcWt6YF7OBZTLwyOVU5oJCgwt0Jiu2HQqFMuOa2FwtCRDLLB2AdNAW54SXj9MI86Xeb23VaGHXXninz00ghx2DAtG',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
