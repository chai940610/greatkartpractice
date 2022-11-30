from django.urls import path
from . import views

urlpatterns = [
    path('', views.store,name='store'),
    path('category/<slug:ab>/',views.store,name='product_by_category'),
    path('category/<slug:ab>/<slug:zakura>/',views.product_detail,name='product_detail'),
]
