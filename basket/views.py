from django.shortcuts import render, redirect, reverse


def basket(request):
    """ View to return shopping basket page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ View to add a quantity of a specified product to the basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size'] 
    basket = request.session.get('basket', {})

    if size:
        if item_id in list(basket.keys()):
            if size in basket[item_id]['items_by_size'].keys():
                basket[item_id]['items_by_size'][size] += quantity
            else:
                basket[item_id]['items_by_size'][size] = quantity
        else:
            basket[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(basket.keys()):
            basket[item_id] += quantity
        else:
            basket[item_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)


    def update_basket(request, item_id):
        """ View to update the quantity of a specified product """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size'] 
    basket = request.session.get('basket', {})

    if size:
        if quantity > 0:
            basket[item_id]['items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{product.name} quantity to '
                              f'{basket[item_id]["items_by_size"][size]}'))
        else:
            del basket[item_id]['items_by_size'][size]
            if not basket[item_id]['items_by_size']:
                basket.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your shopping basket'))
    else:
        if quantity > 0:
            basket[item_id] = quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {basket[item_id]}'))
        else:
            basket.pop(item_id)
            messages.success(request,
                             (f'Removed {product.name} '
                              f'from your shopping basket'))

    request.session['basket'] = basket
    return redirect(reverse('basket'))