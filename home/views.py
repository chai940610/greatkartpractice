from django.shortcuts import render
from store.models import product
#for paginator
from django.core.paginator import Paginator
from store.models import product
from django.db.models import Q

def home(request):
    product1=product.objects.all().filter(availability=True)
    #paginator, these 3 are extremely important, use it everytime, these 3 from django documentation
    babi=Paginator(product1,7)
    nono=request.GET.get('koko')    #behind koko can be anyname, page or what also ok
    paged_product=babi.get_page(nono)
    return render(request,'home/home.html',{'product1':paged_product})

def search(request):
    search_item=None
    if 'bee' in request.GET:
        search_item=request.GET['bee']
        if search_item is not None:
            item=product.objects.filter(Q(product_name__icontains=search_item)|Q(description__icontains=search_item)).order_by('-created_date')
            item_quantity=item.count()
    return render(request,'store/store.html',{'b':item,'product_count':item_quantity,'search_item':search_item})
