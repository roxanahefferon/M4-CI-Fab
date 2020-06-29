from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def all_catalogue(request):
    """ View to show all products in catalogue,
        including sorting and search queries """

    products = Product.objects.all()
    sort = None
    direction = None
    query = None
    categories = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter a search criteria!")
                return redirect(reverse('catalogue'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'catalogue/catalogue.html', context)


def product_description(request, product_id):
    """ View to show a single product from catalogue """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'catalogue/product_description.html', context)


@login_required
def create_product(request):
    """ Creates a new product """
    if not request.user.is_superuser:
        messages.error(request, 'Whoops, only store owners here')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'New product created successfully')
            return redirect(reverse('product_description', args=[product.id]))
        else:
            messages.error(request, 'Failed to create new product')
    else:
        form = ProductForm()

    template = 'catalogue/create_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def update_product(request, product_id):
    """ Edits an existing product """
    if not request.user.is_superuser:
        messages.error(request, 'Whoops, only store owners here')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect(reverse('product_description', args=[product.id]))
        else:
            messages.error(request, 'Failed to update')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'Updating {product.name}')

    template = 'catalogue/update_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Deletes an existing product """
    if not request.user.is_superuser:
        messages.error(request, 'Whoops, only store owners here')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'Product {product.name} has been deleted')

    return redirect(reverse('catalogue'))