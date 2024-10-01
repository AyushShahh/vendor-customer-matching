from django.db import models
from accounts.models import Customer
from product.models import Product


class Watchlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, blank=False, related_name="watchlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name}: {self.product.name}"
