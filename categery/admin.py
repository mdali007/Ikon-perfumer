from django.contrib import admin
from .models import Catagory

# Register category models.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('cat_name',)}
    list_display = ('cat_name', 'slug')

admin.site.register(Catagory, CategoryAdmin)