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

class variationmanager(models.Manager):
    def asura(self):
        return super(variationmanager,self).filter(variation_category='Colour',is_active=True)  #remember this, the variation_category="Colour", the name must be similar to variation_category_choice, ('Colour','colour') the left side must be similar

    def size(self):
        return super(variationmanager,self).filter(variation_category='Size',is_active=True)
    
    def length(self):
        return super().filter(variation_category='Length',is_active=True)

variation_category_choice=( #this is for admin page selection
    ('Colour','colour'),  #the right side one is for admin page, once you fill up in the admin page, it will save it into name shoes, shoes become a category, just abstract, you can't see it
    ('Size','size'),
    ('Length','length'),
)

class variation(models.Model):
    product1=models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=200,choices=variation_category_choice)
    variation_value=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)

    objects=variationmanager()

    def __str__(self):
        return self.variation_value
    