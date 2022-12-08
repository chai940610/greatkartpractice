from django.contrib import admin
from .models import Cart,CartItem

class malaysia(admin.ModelAdmin):
    list_display=('product','cart','quantity')

admin.site.register(Cart)
admin.site.register(CartItem,malaysia)
