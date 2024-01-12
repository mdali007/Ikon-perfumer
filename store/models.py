from django.db import models
from categery.models import Catagory
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    pr_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/product')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # for connecting with catagory model 
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('pr_detail', args=[self.catagory.slug, self.slug])

    def __str__(self):
        return self.pr_name
    

variation_cat_choice =(
    ('size', 'size'),
    ('color', 'color'),
)

class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_cat = models.CharField(max_length=100, choices=variation_cat_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product