from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Avg, Count, Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from product.models import Product, ProductRating, ProductReview, ProductCategory
from business.models import Business
from .models import Watchlist
from accounts.models import Customer


def landing_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect(reverse("customer:home_page"))
        return redirect(reverse("vendor:index"))

    return render(request, 'customer/landing.html')


@login_required
def home_page(request):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    # Get products with high sales in user's area
    popular_products = Product.objects.filter(
        business__area=request.user.area
    ).annotate(
        sales_count=Count('sales')
    ).order_by('-sales_count')[:8]
    
    # Get highly rated products in user's area
    highly_rated_products = Product.objects.filter(
        business__area=request.user.area
    ).annotate(
        average_rating=Avg('ratings__rating')
    ).filter(
        average_rating__isnull=False
    ).order_by('-average_rating')[:8]
    
    # Add average rating to popular products
    for product in popular_products:
        ratings = ProductRating.objects.filter(product=product)
        product.average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'popular_products': popular_products,
        'highly_rated_products': highly_rated_products
    }
    
    return render(request, 'customer/index.html', context)


@login_required
def search_view(request):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    categories = ProductCategory.objects.all()
    areas = Business.objects.values_list('area', flat=True).distinct()
    
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_rating = request.GET.get('min_rating', '')
    area = request.GET.get('area', '')

    if not (query or category_id or min_price or max_price or min_rating or area):
        context = {
        'products': None,
        'categories': categories,
        'areas': areas
        }
        return render(request, 'customer/search.html', context)
    
    # Start with all products
    products = Product.objects.all()
    
    # Apply filters if provided
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(business__name__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if min_price:
        products = products.filter(selling_price__gte=float(min_price))
    
    if max_price:
        products = products.filter(selling_price__lte=float(max_price))
    
    if area:
        products = products.filter(business__area=area)
    
    # Annotate with average ratings
    products = products.annotate(average_rating=Avg('ratings__rating'))
    
    # Filter by minimum rating if specified
    if min_rating:
        products = products.filter(average_rating__gte=float(min_rating))
    
    context = {
        'products': products,
        'categories': categories,
        'areas': areas
    }
    
    return render(request, 'customer/search.html', context)


@login_required
def product_detail(request, product_id):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    product = get_object_or_404(Product, id=product_id)
    
    # Get average rating for this product
    ratings = ProductRating.objects.filter(product=product)
    product.average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    # Check if product is in user's watchlist
    customer = get_object_or_404(Customer, id=request.user.id)
    is_in_watchlist = Watchlist.objects.filter(user=customer, product=product).exists()
    
    # Get all reviews for this product with ratings
    reviews = ProductReview.objects.filter(product=product)
    for review in reviews:
        try:
            review.rating = ProductRating.objects.get(user=review.user, product=product).rating
        except ProductRating.DoesNotExist:
            review.rating = None
            
    # Check if user has already reviewed the product
    user_reviewed = ProductReview.objects.filter(user=customer, product=product).exists()
    
    context = {
        'product': product,
        'reviews': reviews,
        'is_in_watchlist': is_in_watchlist,
        'user_can_review': not user_reviewed
    }
    
    return render(request, 'customer/product_detail.html', context)


@login_required
def add_to_watchlist(request, product_id):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        customer = get_object_or_404(Customer, id=request.user.id)
        
        # Check if product is already in watchlist
        if not Watchlist.objects.filter(user=customer, product=product).exists():
            Watchlist.objects.create(user=customer, product=product)
            messages.success(request, f"{product.name} added to your watchlist!")
        else:
            messages.info(request, "This product is already in your watchlist.")
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('customer:product_detail', args=[product_id])))


@login_required
def remove_from_watchlist(request, product_id):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        customer = get_object_or_404(Customer, id=request.user.id)
        
        # Find and delete watchlist entry
        try:
            watchlist_item = Watchlist.objects.get(user=customer, product=product)
            watchlist_item.delete()
            messages.success(request, f"{product.name} removed from your watchlist.")
        except Watchlist.DoesNotExist:
            messages.error(request, "This product wasn't in your watchlist.")
    
    # If we came from the watchlist page and that's the only item, go back to watchlist
    if 'watchlist' in request.META.get('HTTP_REFERER', ''):
        return redirect(reverse('customer:watchlist'))
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('customer:product_detail', args=[product_id])))


@login_required
def watchlist_view(request):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    customer = get_object_or_404(Customer, id=request.user.id)
    watchlist_items = Watchlist.objects.filter(user=customer)
    
    # Add average rating to each product
    for item in watchlist_items:
        ratings = ProductRating.objects.filter(product=item.product)
        item.product.average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'watchlist_items': watchlist_items
    }
    
    return render(request, 'customer/watchlist.html', context)


@login_required
def add_review(request, product_id):
    if request.user.user_type != 'customer':
        return redirect(reverse("vendor:index"))
    
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        customer = get_object_or_404(Customer, id=request.user.id)
        rating_value = int(request.POST.get('rating', 0))
        review_text = request.POST.get('review', '').strip()
        
        # Validate rating is between 1 and 5
        if not 1 <= rating_value <= 5:
            messages.error(request, "Rating must be between 1 and 5.")
            return redirect(reverse('customer:product_detail', args=[product_id]))
            
        # Check if customer already reviewed this product
        if ProductReview.objects.filter(user=customer, product=product).exists():
            messages.error(request, "You have already reviewed this product.")
            return redirect(reverse('customer:product_detail', args=[product_id]))
        
        # Create rating
        ProductRating.objects.create(
            user=customer,
            product=product,
            rating=rating_value
        )
        
        # Create review if text provided
        if review_text:
            ProductReview.objects.create(
                user=customer,
                product=product,
                review=review_text
            )
        
        messages.success(request, "Thank you for your review!")
    
    return redirect(reverse('customer:product_detail', args=[product_id]))
