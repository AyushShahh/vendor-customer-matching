from django.contrib import admin
from .models import CustomUser, Customer, Vendor


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'user_type',  'area', 'city', 'is_staff')
    search_fields = ('id', 'email', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_staff', 'city', 'area')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Vendor)
