from django.shortcuts import render,get_object_or_404
from .models import category,product
from django.http import Http404

def store(request,ab=None):
    a=None
    b=None
    if ab != None:
        a=get_object_or_404(category,slug=ab)
        b=product.objects.filter(category1=a,availability=True)
        product_count=b.count()
    else:
        b=product.objects.all().filter(availability=True)
        product_count=b.count()
    return render(request,'store/store.html',{'b':b,'product_count':product_count})

def product_detail(request,ab,zakura,single_product=None):
    try:    # The try block lets you test a block of code for errors.
        single_product=product.objects.get(category1__slug=ab,slug=zakura)
    except Exception as e: #The except block lets you handle the error. exception as e for my guessing is handle all kind of error
        raise Http404('Invalid Product')
    return render(request,'store/product_detail.html',{'single_product':single_product})
