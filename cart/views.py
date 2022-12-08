from django.shortcuts import render,redirect,get_object_or_404
from store.models import product,variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

#get the cart id
def _cart_id(request):
    #request the session key from the URL
    cart=request.session.session_key    #if the session key didn't find in the database, then create it
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id,cart_item=None):    #since we need to add the product inside the cart, so we need assign a product_id
    # colour=request.POST['colour']
    # size=request.POST['size']
    # return HttpResponse('hello')
    product2=product.objects.get(availability=True,id=product_id)
    product_variation=[]
    if request.method == "POST":
        for abc in request.POST:
            key=abc
            value=request.POST[key]
            # print(key,value)
            try:
                variation1=variation.objects.get(product1=product2,variation_category__iexact=key,variation_value__iexact=value)  #check the variation_category correct or not
                # print(variation1)
                product_variation.append(variation1)    #this product_variation we need save it into cart item
            except:  
                pass          
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    #another try and except for CartItem
    #check if the cartitem exist or not
    is_cart_item_exists=CartItem.objects.filter(product=product2,cart=cart).exists()
    if is_cart_item_exists:
        cart_item=CartItem.objects.filter(cart=cart,product=product2)
        ad=[]
        ex_var_list=[]
        for abc in cart_item:
            existing_variation=abc.variations.all()
            ex_var_list.append(list(existing_variation))  #existing_variation inside all things will move into ex_var_list
            ad.append(abc.id)
            # print(ex_var_list), the answer quite similar without the list, when ex_var_list.append(list(existing_variation))
            # [[<variation: ghost>, <variation: large>, <variation: short>]]
            # [[<variation: ghost>, <variation: large>, <variation: short>], [<variation: blue>, <variation: small>, <variation: long>]]
            # [[<variation: ghost>, <variation: large>, <variation: short>], [<variation: blue>, <variation: small>, <variation: long>], []]
            # [[<variation: ghost>, <variation: large>, <variation: short>], [<variation: blue>, <variation: small>, <variation: long>], [], []]
            # [[<variation: ghost>, <variation: large>, <variation: short>], [<variation: blue>, <variation: small>, <variation: long>], [], [], []]
            # [[<variation: ghost>, <variation: large>, <variation: short>], [<variation: blue>, <variation: small>, <variation: long>], [], [], [], [<variation: large>, <variation: long>, <variation: Purple>]]
            #print(ex_var_list)  # the answer in terminal, when ex_var_list.append(existing_variation)
                                # [<QuerySet [<variation: ghost>, <variation: large>, <variation: short>]>]
                                # [<QuerySet [<variation: ghost>, <variation: large>, <variation: short>]>, <QuerySet [<variation: blue>, <variation: small>, <variation: long>]>]
                                # [<QuerySet [<variation: ghost>, <variation: large>, <variation: short>]>, <QuerySet [<variation: blue>, <variation: small>, <variation: long>]>, <QuerySet []>]
                                # [<QuerySet [<variation: ghost>, <variation: large>, <variation: short>]>, <QuerySet [<variation: blue>, <variation: small>, <variation: long>]>, <QuerySet []>, <QuerySet []>]
                                # [<QuerySet [<variation: ghost>, <variation: large>, <variation: short>]>, <QuerySet [<variation: blue>, <variation: small>, <variation: long>]>, <QuerySet []>, <QuerySet []>, <QuerySet []>]
            #print(ad)       # the answer show in terminal , 
                            # [21]
                            # [21, 22]
                            # [21, 22, 23]
                            # [21, 22, 23, 24]
                            # [21, 22, 23, 24, 25]
                            # know why? because there are 5 cart item with similar cart number, so 5 id is here
        #check whether the product_variation is empty or not, if no we can safely add to the cart item
        #existing variation
        #product variation
        #item id
        if product_variation in ex_var_list:    # if product_variation user tekan inside the database exist
            index=ex_var_list.index(product_variation)  
            #return HttpResponse(index)  unbelieveable the answer is 0, when i choose ghost,large,short, the answer is 1 when i choose blue,small,long
            item_id=ad[index]   #example ad=[31,32,33] index=[2], so ad[index]=33
            #return HttpResponse(index) when i choose ghost small short, the index is 5, know why? the index are looking for which cart item have the product_variation attribute, they are same, at the end the cart item number 5 have it, so index is 5
            #return HttpResponse(item_id)    return the cartItem id, when I choose ghost small short, it will look which cartitem id have this variation, at the end no 27 cartitem have
            item=CartItem.objects.get(product=product2,pk=item_id)  #get which product, with the exact cartitem ID
            item.quantity+=1
            item.save()
        else:
            #if variation don't exist in current cart item?
            item=CartItem.objects.create(product=product2,quantity=1,cart=cart)
            if len(product_variation)>0:
                item.variations.clear()
            #loop thru the product variation, due to they have key and value and many item, so we must loop all of these
                item.variations.add(*product_variation) # * mean make sure all the product_variation will be added
        # cart_item.quantity+=1
            item.save()
    else:
            cart_item=CartItem.objects.create(
            cart=cart,
            product=product2,
            quantity=1,
            )
            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
                cart_item.save()
    return redirect('cart')

def cart(request,grand_total=0,total=0,total_quantity=0,cart_item=None,tax=0):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.filter(cart=cart,is_active=True)
        for abc in cart_item:
            total+=(abc.product.price*abc.quantity)
            total_quantity+=abc.quantity
        tax=(total*0.06)
        grand_total=tax+total
    except ObjectDoesNotExist:
        pass
    return render(request,'cart/cart.html',{'grand_total':grand_total,'tax':tax,'cart_item':cart_item,'total':total,'total_quantity':total_quantity})

def remove_cart(request,sampah,tikus):
    product2=product.objects.get(id=tikus)
    try:
        cart_item=CartItem.objects.get(product=product2,id=sampah)
        # cart=Cart.objects.get(cart_id=_cart_id(request))
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('cart')

def remove_cart_item(request,bird,goku):
    product3=product.objects.get(id=bird)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product3,cart=cart,pk=goku)
        cart_item.delete()
    except:
        pass
    return redirect('cart')