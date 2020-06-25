from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There are no items in your shopping basket at the moment")
        return redirect(reverse('catalogue'))

        order_form = OrderForm()  # instance of the order form
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
        }

        return render(request, template, context )
