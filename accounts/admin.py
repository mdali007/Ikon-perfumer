from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'f_name', 'l_name', 'username', 'last_login', 'date_joined', 'is_active',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)