from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from catalogue.models import Product
from django.contrib import messages


def basket(request):
    """ View to return shopping basket page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ View to add a quantity of a specified product to the basket """

    product = get_object_or_404(Product, pk=item_id)
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
                messages.success(request, f'{product.name} {size.upper()} was updated to: {basket[item_id]["items_by_size"][size]}')
        else:
            basket[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'{product.name} {size.upper()} was added to your shopping basket')
    else:
        if item_id in list(basket.keys()):
            basket[item_id] += quantity
            messages.success(request, f'{product.name} quantity was updated to: {basket[item_id]}')
        else:
            basket[item_id] = quantity
            messages.success(request, f'{product.name} was added to your shopping basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def update_basket(request, item_id):
    """ View to update the quantity of a specified product """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size'] 
    basket = request.session.get('basket', {})

    if size:
        if quantity > 0:
            basket[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'{product.name} {size.upper()} was updated to: {basket[item_id]["items_by_size"][size]}')
        else:
            del basket[item_id]['items_by_size'][size]
            if not basket[item_id]['items_by_size']:
                basket.pop(item_id)
                messages.success(request, f'{product.name} {size.upper()} was deleted from your shopping basket')
    else:
        if quantity > 0:
            basket[item_id] = quantity
            messages.success(request, f'{product.name} quantity was updated to: {basket[item_id]}')
        else:
            basket.pop(item_id)
            messages.success(request, f'{product.name} was deleted from your shopping basket')

    request.session['basket'] = basket
    return redirect(reverse('basket'))


def delete_basket(request, item_id):
    """ View to delete a specified product from shopping basket """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size'] 
        basket = request.session.get('basket', {})

        if size:
            del basket[item_id]['items_by_size'][size]
            if not basket[item_id]['items_by_size']:
                basket.pop(item_id)
            messages.success(request, f'{product.name} {size.upper()} was deleted from your shopping basket')
        else:
            basket.pop(item_id)
            messages.success(request, f'{product.name} was deleted from your shopping basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'An error ocurred while removing the item:(e)')
        return HttpResponse(status=500)
