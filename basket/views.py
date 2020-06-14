from django.shortcuts import render, redirect


def basket(request):
    """ View to return shopping basket page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ View to add a quantity of a specified product to the basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        basket[item_id] += quantity
    else:
        basket[item_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)
