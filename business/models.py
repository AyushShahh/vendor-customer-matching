from django.db import models
from accounts.models import Vendor, Customer


class Business(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    description = models.CharField(max_length=400, null=False, blank=False)
    city = models.CharField(max_length=20, null=False, blank=False)
    area = models.CharField(max_length=20, null=False, blank=False)
    state = models.CharField(max_length=20, null=False, blank=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey('BusinessCategory', related_name="businesses", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class BusinessRating(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="business_ratings")
    shop = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(blank=False, null=False)

    def clean(self):
        if not (1 <= self.rating <= 10):
            raise ValueError('Rating must be between 1 and 10')

    def __str__(self):
        return f"{self.user.first_name} rated {self.shop.name} {self.rating}"

class BusinessReview(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="business_reviews")
    shop = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews")
    review = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name}'s review on {self.shop.name}"


class BusinessCategory(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.name
