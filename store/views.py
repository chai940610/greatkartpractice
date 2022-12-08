from django.shortcuts import render,get_object_or_404
from .models import category,product
from django.http import Http404,HttpResponse
from cart.models import CartItem,Cart
from cart.views import _cart_id
#for paginator
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

def store(request,ab=None):
    a=None
    b=None
    if ab != None:
        a=get_object_or_404(category,slug=ab)
        b=product.objects.filter(category1=a,availability=True)
        paginator=Paginator(b,3)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count=b.count()
    else:
        b=product.objects.all().filter(availability=True).order_by('-pk')
        paginator=Paginator(b,3)
        page=request.GET.get('page')    #get the url that catch the page number
        paged_product=paginator.get_page(page)
        product_count=b.count()
    return render(request,'store/store.html',{'b':paged_product,'product_count':product_count})

def product_detail(request,ab,zakura,single_product=None):
    try:    # The try block lets you test a block of code for errors.
        single_product=product.objects.get(category1__slug=ab,slug=zakura)
        #let check the item in the cart item or not
        check_item=CartItem.objects.filter(product=single_product,cart__cart_id=_cart_id(request)).exists()
        #if check_item is true, we not gonna show the cart
        # return HttpResponse(check_item)
    except Exception as e: #The except block lets you handle the error. exception as e for my guessing is handle all kind of error
        raise Http404('Invalid Product')
    return render(request,'store/product_detail.html',{'check_item':check_item,'single_product':single_product})
