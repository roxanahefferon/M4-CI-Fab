from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_catalogue(request):
    """ View to show all products in catalogue, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'catalogue/catalogue.html', context)


def product_description(request, product_id):
    """ View to show a single product from catalogue """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'catalogue/product_description.html', context)