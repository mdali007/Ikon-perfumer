from django.contrib import admin
from .models import Product, Variations

# Register your models here.
class PrAdmin(admin.ModelAdmin):
    list_display = ('pr_name', 'price', 'stock', 'catagory', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('pr_name',)}


class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_value', 'variation_cat', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_value', 'variation_cat', 'is_active')

admin.site.register(Product, PrAdmin)
admin.site.register(Variations, VariationsAdmin)