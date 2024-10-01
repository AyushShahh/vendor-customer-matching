from django.contrib import admin
from .models import Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'selling_price', 'timestamp')
    list_filter = ('product', 'selling_price', 'quantity')


admin.site.register(Sale, SaleAdmin)
