from django.contrib import admin
from .models import Business, BusinessReview, BusinessRating, BusinessCategory


class BusinessAdmin(admin.ModelAdmin):
     list_display = ('id', 'name', 'vendor', 'area', 'city', 'category')
     search_fields = ('name', 'vendor', 'id')
     list_filter = ('area', 'city', 'category')

class BusinessRatingAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'shop', 'rating')
     list_filter = ('rating', 'user', 'shop')

class BusinessReviewAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'shop', 'review')
     search_fields = ('id', 'review')
     list_filter = ('shop', 'user')

class BusinessCategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('id', 'name')


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessRating, BusinessRatingAdmin)
admin.site.register(BusinessReview, BusinessReviewAdmin)
admin.site.register(BusinessCategory, BusinessCategoryAdmin)
