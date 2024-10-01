from django.db import models
from business.models import Business
from accounts.models import Customer


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, blank=False, null=False, related_name="products")
    description = models.TextField(max_length=250, blank=False, null=False)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name


class ProductRating(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="product_ratings")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(blank=False, null=False)

    def clean(self):
        if not (1 <= self.rating <= 10):
            raise ValueError('Rating must be between 1 and 10')

    def __str__(self):
        return f"{self.user.first_name} rated {self.product.name} {self.rating}"


class ProductReview(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="product_reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    review = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name}'s review on {self.product.name}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name
