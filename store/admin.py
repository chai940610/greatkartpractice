from django.contrib import admin
from .models import category,product

class saham(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=['category_name','slug']

class koko(admin.ModelAdmin):
    list_display=('product_name','price','stock','category1','modified_date','availability')
    prepopulated_fields={'slug':('product_name',)}
admin.site.register(category,saham)
admin.site.register(product,koko)
