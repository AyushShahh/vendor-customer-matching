from django.contrib import admin
from .models import Business, BusinessReview, BusinessRating, BusinessCategory


class BusinessAdmin(admin.ModelAdmin):
     list_display = ('id', 'name', 'vendor', 'area', 'city', 'category')
     search_fields = ('name', 'vendor', 'id')
     list_filter = ('area', 'city', 'category')

class BusinessCategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('id', 'name')


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessCategory, BusinessCategoryAdmin)
