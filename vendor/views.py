from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, F, Q, Avg
from django.http import JsonResponse
from accounts.models import Vendor
from business.models import Business, BusinessCategory
from product.models import Product, ProductCategory
from .models import Sale
from .forms import BusinessForm, ProductForm, SaleForm
from django.db.models.functions import TruncDay, TruncMonth


def vendor_required(view_func):
    """Decorator to ensure only vendors can access certain views."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'vendor':
            messages.error(request, "You must be a vendor to access this page.")
            return redirect('customer:landing_page')
        return view_func(request, *args, **kwargs)
    return wrapper


@vendor_required
def index(request):
    """Vendor Dashboard/Overview"""
    vendor = request.user.vendor
    businesses = Business.objects.filter(vendor=vendor)
    total_businesses = businesses.count()
    
    # Get all products across all businesses
    products = Product.objects.filter(business__vendor=vendor)
    total_products = products.count()
    
    # Get low inventory products (quantity < 10)
    low_inventory = products.filter(quantity__lt=10, quantity__gt=0).count()
    
    # Get out of stock products
    out_of_stock = products.filter(quantity=0).count()
    
    # Get total sales and profit
    total_sales = Sale.get_total_revenue(period='month')
    total_profit = Sale.get_total_profit(period='month')
    
    context = {
        'total_businesses': total_businesses,
        'total_products': total_products,
        'low_inventory': low_inventory,
        'out_of_stock': out_of_stock,
        'total_sales': total_sales,
        'total_profit': total_profit,
    }
    
    return render(request, 'vendor/index.html', context)


@vendor_required
def business_list(request):
    """List all businesses owned by the vendor"""
    vendor = request.user.vendor
    businesses = Business.objects.filter(vendor=vendor)
    
    context = {
        'businesses': businesses,
    }
    
    return render(request, 'vendor/business_list.html', context)


@vendor_required
def business_create(request):
    """Create a new business"""
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.vendor = request.user.vendor
            business.save()
            messages.success(request, f"Business '{business.name}' created successfully.")
            return redirect('vendor:business_detail', business_id=business.id)
    else:
        form = BusinessForm()
    
    context = {
        'form': form,
        'title': 'Create Business',
    }
    
    return render(request, 'vendor/business_form.html', context)


@vendor_required
def business_detail(request, business_id):
    """View details of a specific business"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    
    # Get business stats
    products = Product.objects.filter(business=business)
    total_products = products.count()
    low_inventory = products.filter(quantity__lt=10, quantity__gt=0).count()
    out_of_stock = products.filter(quantity=0).count()
    
    # Get sales data
    total_sales = Sale.get_total_revenue(business_id=business.id, period='month')
    total_profit = Sale.get_total_profit(business_id=business.id, period='month')
    
    # Get customer ratings and reviews
    average_rating = business.ratings.aggregate(avg_rating=Sum('rating') / Count('rating'))['avg_rating'] if business.ratings.exists() else 0
    recent_reviews = business.reviews.order_by('-id')[:5]
    
    context = {
        'business': business,
        'total_products': total_products,
        'low_inventory': low_inventory,
        'out_of_stock': out_of_stock,
        'total_sales': total_sales,
        'total_profit': total_profit,
        'average_rating': average_rating,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'vendor/business_detail.html', context)


@vendor_required
def business_edit(request, business_id):
    """Edit a business"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    
    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, f"Business '{business.name}' updated successfully.")
            return redirect('vendor:business_detail', business_id=business.id)
    else:
        form = BusinessForm(instance=business)
    
    context = {
        'form': form,
        'business': business,
        'title': 'Edit Business',
    }
    
    return render(request, 'vendor/business_form.html', context)


@vendor_required
def business_delete(request, business_id):
    """Delete a business"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    
    if request.method == 'POST':
        business_name = business.name
        business.delete()
        messages.success(request, f"Business '{business_name}' deleted successfully.")
        return redirect('vendor:business_list')
    
    context = {
        'business': business,
    }
    
    return render(request, 'vendor/business_confirm_delete.html', context)


@vendor_required
def product_list(request, business_id):
    """List all products for a specific business"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    products = Product.objects.filter(business=business)
    
    context = {
        'business': business,
        'products': products,
    }
    
    return render(request, 'vendor/product_list.html', context)


@vendor_required
def product_create(request, business_id):
    """Create a new product for a specific business"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            messages.success(request, f"Product '{product.name}' added successfully.")
            return redirect('vendor:product_list', business_id=business.id)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'business': business,
        'title': 'Add Product',
    }
    
    return render(request, 'vendor/product_form.html', context)


@vendor_required
def product_edit(request, business_id, product_id):
    """Edit a product"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    product = get_object_or_404(Product, id=product_id, business=business)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('vendor:product_list', business_id=business.id)
    else:
        form = ProductForm(instance=product)
    
    # --- Analytics ---
    sales = Sale.objects.filter(product=product)
    total_sales = sales.aggregate(total=Sum('quantity'))['total'] or 0
    total_revenue = sales.aggregate(total=Sum(F('quantity') * F('selling_price')))['total'] or 0
    average_rating = product.ratings.aggregate(avg=Avg('rating'))['avg'] if hasattr(product, 'ratings') else None

    # Monthly sales for chart (last 6 months)
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.now().date()
    months = []
    sales_data = []
    for i in range(5, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        month_label = month_start.strftime('%b %Y')
        months.append(month_label)
        month_sales = sales.filter(timestamp__date__gte=month_start, timestamp__date__lte=month_end).aggregate(total=Sum('quantity'))['total'] or 0
        sales_data.append(month_sales)

    context = {
        'form': form,
        'business': business,
        'product': product,
        'title': 'Edit Product',
        'product_analytics': {
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'average_rating': average_rating,
            'months': months,
            'sales_data': sales_data,
        }
    }
    
    return render(request, 'vendor/product_form.html', context)


@vendor_required
def product_delete(request, business_id, product_id):
    """Delete a product"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    product = get_object_or_404(Product, id=product_id, business=business)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully.")
        return redirect('vendor:product_list', business_id=business.id)
    
    context = {
        'business': business,
        'product': product,
    }
    
    return render(request, 'vendor/product_confirm_delete.html', context)


@vendor_required
def create_sale(request, business_id):
    """Create a new sale for a product"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    
    if request.method == 'POST':
        form = SaleForm(request.POST, business=business)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            
            # Check if there's enough inventory
            if product.quantity < quantity:
                messages.error(request, f"Not enough stock for {product.name}. Only {product.quantity} available.")
                return redirect('vendor:create_sale', business_id=business.id)
            
            # Create the sale
            sale = Sale(
                product=product,
                quantity=quantity,
                selling_price=product.selling_price
            )
            sale.save()
            
            # Update product quantity
            product.quantity -= quantity
            product.save()
            
            messages.success(request, f"Sale of {quantity} {product.name}(s) recorded successfully.")
            return redirect('vendor:product_list', business_id=business.id)
    else:
        form = SaleForm(business=business)
    
    context = {
        'form': form,
        'business': business,
        'title': 'Record Sale',
    }
    
    return render(request, 'vendor/sale_form.html', context)


@vendor_required
def sales_history(request, business_id):
    """View sales history for a specific business"""
    vendor = request.user.vendor
    business = get_object_or_404(Business, id=business_id, vendor=vendor)
    
    # Filter by time period if provided
    period = request.GET.get('period', 'month')
    sales = Sale.get_sales_for_business(business_id=business.id, period=period)
    
    total_revenue = Sale.get_total_revenue(business_id=business.id, period=period)
    total_profit = Sale.get_total_profit(business_id=business.id, period=period)

    # Aggregate sales for chart (group by day or month based on period)
    if period in ['month', 'week', 'today']:
        sales_agg = sales.annotate(day=TruncDay('timestamp')).values('day').annotate(total=Sum('quantity')).order_by('day')
        chart_labels = [s['day'].strftime('%b %d') for s in sales_agg]
        chart_data = [s['total'] for s in sales_agg]
    else:
        sales_agg = sales.annotate(month=TruncMonth('timestamp')).values('month').annotate(total=Sum('quantity')).order_by('month')
        chart_labels = [s['month'].strftime('%b %Y') for s in sales_agg]
        chart_data = [s['total'] for s in sales_agg]

    context = {
        'business': business,
        'sales': sales,
        'period': period,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    
    return render(request, 'vendor/sales_history.html', context)


@vendor_required
def analytics(request):
    """View analytics across all businesses using real data."""
    vendor = request.user.vendor
    businesses = Business.objects.filter(vendor=vendor)
    
    period = request.GET.get('period', 'month')
    
    total_businesses = businesses.count()
    total_products = Product.objects.filter(business__vendor=vendor).count()
    low_inventory = Product.objects.filter(business__vendor=vendor, quantity__lt=10, quantity__gt=0).count()
    out_of_stock = Product.objects.filter(business__vendor=vendor, quantity=0).count()
    
    total_revenue = Sale.get_total_revenue(period=period)
    total_profit = Sale.get_total_profit(period=period)
    
    business_data = []
    for business in businesses:
        business_revenue = Sale.get_total_revenue(business_id=business.id, period=period)
        business_profit = Sale.get_total_profit(business_id=business.id, period=period)
        business_data.append({
            'name': business.name,
            'revenue': business_revenue,
            'profit': business_profit,
        })
    if not business_data:
        business_data = [{'name': 'No Data', 'revenue': 0, 'profit': 0}]
    
    low_stock_products = Product.objects.filter(business__vendor=vendor, quantity__lt=10, quantity__gt=0)
    
    from datetime import timedelta
    from django.utils import timezone
    date_filter = Q()
    if period == 'today':
        date_filter = Q(sales__timestamp__date=timezone.now().date())
    elif period == 'week':
        date_filter = Q(sales__timestamp__date__gte=timezone.now().date() - timedelta(days=7))
    elif period == 'month':
        date_filter = Q(sales__timestamp__date__gte=timezone.now().date() - timedelta(days=30))
    
    top_products = list(Product.objects.filter(business__vendor=vendor)
                         .filter(date_filter)
                         .annotate(total_quantity=Sum('sales__quantity'))
                         .order_by('-total_quantity')[:5]
                         .values('name', 'total_quantity'))
    
    context = {
        'total_businesses': total_businesses,
        'total_products': total_products,
        'low_inventory': low_inventory,
        'out_of_stock': out_of_stock,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'business_data': business_data,
        'low_stock_products': low_stock_products,
        'category_data': list(Product.objects.filter(business__vendor=vendor)
                               .values('category__name')
                               .annotate(count=Count('id'))),
        'top_products': top_products,
        'period': period,
    }
    
    return render(request, 'vendor/analytics.html', context)
