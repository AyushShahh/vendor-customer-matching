from django.db import models
from product.models import Product


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, related_name="sales")
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name}, quantity={self.quantity}"
