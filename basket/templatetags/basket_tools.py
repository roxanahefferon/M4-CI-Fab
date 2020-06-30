from django import template


register = template.Library()


@register.filter(name='calc_basket_subtotal')
def calc_basket_subtotal(price, quantity):
    return price * quantity
