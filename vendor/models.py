from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta
from product.models import Product
from business.models import Business


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, related_name="sales")
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name}, quantity={self.quantity}"
    
    def get_total_price(self):
        """Calculate the total price of this sale"""
        return self.quantity * self.selling_price
    
    @classmethod
    def get_sales_for_business(cls, business_id, period=None):
        """Get all sales for a specific business with optional time period filter"""
        sales = cls.objects.filter(product__business_id=business_id)
        
        if period:
            if period == 'today':
                sales = sales.filter(timestamp__date=timezone.now().date())
            elif period == 'week':
                sales = sales.filter(timestamp__date__gte=timezone.now().date() - timedelta(days=7))
            elif period == 'month':
                sales = sales.filter(timestamp__date__gte=timezone.now().date() - timedelta(days=30))
        
        return sales
    
    @classmethod
    def get_total_revenue(cls, business_id=None, period=None):
        """Calculate total revenue for all businesses or a specific business"""
        sales = cls.objects.all()
        
        if business_id:
            sales = sales.filter(product__business_id=business_id)
            
        if period:
            if period == 'today':
                sales = sales.filter(timestamp__date=timezone.now().date())
            elif period == 'week':
                sales = sales.filter(timestamp__date__gte=timezone.now().date() - timedelta(days=7))
            elif period == 'month':
                sales = sales.filter(timestamp__date__gte=timezone.now().date() - timedelta(days=30))
        
        revenue = sales.aggregate(
            total=Sum(F('quantity') * F('selling_price'))
        )['total'] or 0
        
        return revenue
    
    @classmethod
    def get_total_profit(cls, business_id=None, period=None):
        """Calculate total profit for all businesses or a specific business"""
        sales = cls.objects.all()
        
        if business_id:
            sales = sales.filter(product__business_id=business_id)
            
        if period:
            if period == 'today':
                sales = sales.filter(timestamp__date=timezone.now().date())
            elif period == 'week':
                sales = sales.filter(timestamp__date__gte=timezone.now().date() - timedelta(days=7))
            elif period == 'month':
                sales = sales.filter(timestamp__date__gte=timezone.now().date() - timedelta(days=30))
        
        # Calculate profit as (selling_price - cost_price) * quantity
        profit = sales.annotate(
            item_profit=ExpressionWrapper(
                (F('selling_price') - F('product__cost_price')) * F('quantity'),
                output_field=DecimalField()
            )
        ).aggregate(total=Sum('item_profit'))['total'] or 0
        
        return profit
