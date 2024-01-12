from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_item = CartItem.objects.all().filter(cart=cart[:1])
            for cart_it in cart_item:
                count += cart_it.quantity
        except Cart.DoesNotExist:
            count = 0
    return dict(c_count=count)
