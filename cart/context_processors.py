from cart.models import CartItem,Cart
from cart.views import _cart_id

def susu(request):
    cart_item=CartItem.objects.filter(cart__cart_id=_cart_id(request))
    total_quantity=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            for abc in cart_item:
                total_quantity= abc.quantity+total_quantity
        except CartItem.DoesNotExist:
            total_quantity=0
    return dict(total_quantity=total_quantity)