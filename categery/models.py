from django.db import models
from django.urls import reverse

# categery model
class Catagory(models.Model):
    cat_name = models.CharField(max_length=100, unique=True)
    cat_discription = models.TextField(max_length=250, blank=True)
    cat_image = models.ImageField(upload_to='photos/category', blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def get_url(self):
        return reverse('pr_by_cat', args=[self.slug])

    def __str__(self) :
        return self.cat_name