from django import template
from main.models import Category,Cart
from accounts.models import Currency
register = template.Library()



register=template.Library()



@register.inclusion_tag('base/category.html',takes_context=False)
def categories():
    categories=Category.objects.only('name')
    return{'categories':categories}



@register.inclusion_tag('base/cart_num.html', takes_context=True)
def cart_num(context):
    try:
        request_user = context['request'].user
        cart = Cart.objects.get(user=request_user, complete=False)
        cart_items = cart.cartitems.all()
        num_items = sum(item.quantity for item in cart_items)
        return {'num_items': num_items}
    except (KeyError, Cart.DoesNotExist):
        return {'num_items': 0}


@register.inclusion_tag('base/currency.html',takes_context=True)
def currency(context):
    currency=Currency.objects.all()
    return{'currencies':currency}



@register.filter(name='convert')
def convert_currency(price, currency_exchange_rate):
    if currency_exchange_rate:
        rate=float(currency_exchange_rate)
        price=float(price)
        return round(price * rate, 2)
    return price