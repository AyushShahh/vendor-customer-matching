from django.contrib import admin
from .models import Product, ProductReview, ProductRating, ProductCategory


class ProductAdmin(admin.ModelAdmin):
     list_display = ('id', 'name', 'business', 'quantity', 'cost_price', 'selling_price', 'category')
     search_fields = ('name', 'id')
     list_filter = ('business', 'category', 'cost_price', 'selling_price', 'quantity')

class ProductRatingAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'product', 'rating')
     list_filter = ('rating', 'user', 'product')

class ProductReviewAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'product', 'review')
     search_fields = ('id', 'review')
     list_filter = ('product', 'user')

class ProductCategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('id', 'name')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductRating, ProductRatingAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
