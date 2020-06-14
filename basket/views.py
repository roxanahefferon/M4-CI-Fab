from django.shortcuts import render


def basket(request):
    """ View to return shopping basket page """

    return render(request, 'basket/basket.html')
