from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('remove_cart/<int:sampah>/<int:tikus>/',views.remove_cart,name='remove_cart'), #remember that when there are two pk, you have to input two pk in {% url pk pk %}
    path('remove_cart_item/<int:bird>/<int:goku>',views.remove_cart_item,name='remove_cart_item'),
]
