from cart.views import get_cart
from listings.models import Category
from decimal import Decimal

def cart(request):
    cart = get_cart(request)
    cart_total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
    return {
        'cart_total_price': cart_total_price
    }
    

def categories_processors(request):
    return {'categories': Category.objects.all()}