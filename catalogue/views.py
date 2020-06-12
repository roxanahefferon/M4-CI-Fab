from django.shortcuts import render
from .models import Product

# Create your views here.

def all_catalogue(request):
    """ View to show all products in catalogue, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'catalogue/catalogue.html', context)