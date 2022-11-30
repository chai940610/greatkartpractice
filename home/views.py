from django.shortcuts import render
from store.models import product

def home(request):
    product1=product.objects.all().filter(availability=True)
    return render(request,'home/home.html',{'product1':product1})
