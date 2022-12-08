from django.db import models
from accounts.models import Account
from store.models import product,variation

#create cart and cartitem models
class Cart(models.Model):
    cart_id=models.CharField(max_length=300,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    is_active=models.BooleanField(default=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    variations=models.ManyToManyField(variation,blank=True)

    def __str__(self):
        return self.product.product_name
    
    def sub_total(self):
        return self.product.price*self.quantity