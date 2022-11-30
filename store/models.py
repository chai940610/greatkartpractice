from django.db import models
from django.urls import reverse

class category(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField()
    category_image=models.ImageField(upload_to='photo/category/',blank=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    
    def x(self):
        return reverse('product_by_category',args=[self.slug])

class product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    price=models.FloatField()
    photo=models.ImageField(upload_to='photos/product')
    stock=models.PositiveIntegerField()
    availability=models.BooleanField(default=True)
    category1=models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail',args=[self.category1.slug,self.slug])

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name='product'
        verbose_name_plural='products'