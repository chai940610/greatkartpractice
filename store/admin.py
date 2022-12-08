from django.contrib import admin
from .models import category,product,variation

class saham(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=['category_name','slug']

class koko(admin.ModelAdmin):
    list_display=('product_name','price','stock','category1','modified_date','availability')
    prepopulated_fields={'slug':('product_name',)}

class shit(admin.ModelAdmin):
    list_display=('product1','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product1','variation_category','variation_value')

admin.site.register(category,saham)
admin.site.register(product,koko)
admin.site.register(variation,shit)
