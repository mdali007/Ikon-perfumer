from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery

# @admin_thumbnails.thumbnail('image')
# class ProductGalleryInline(admin.TabularInline):
#     model = ProductGallery
#     extra = 1

class VariationAdmin(admin.ModelAdmin):
    list_display = ('variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('variation_category', 'variation_value')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available', 'price_medium', 'price_large')
    prepopulated_fields = {'slug': ('product_name',)}




admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductGallery)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)

admin.site._registry.pop(Variation)
admin.site._registry.pop(Product)
admin.site._registry.pop(ReviewRating)
admin.site._registry.pop(ProductGallery)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)

