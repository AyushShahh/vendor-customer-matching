from django.urls import path
from . import views

app_name = 'vendor'

urlpatterns = [
    # Dashboard/Overview
    path('', views.index, name="index"),
    
    # Business Management
    path('businesses/', views.business_list, name='business_list'),
    path('businesses/create/', views.business_create, name='business_create'),
    path('businesses/<int:business_id>/', views.business_detail, name='business_detail'),
    path('businesses/<int:business_id>/edit/', views.business_edit, name='business_edit'),
    path('businesses/<int:business_id>/delete/', views.business_delete, name='business_delete'),
    
    # Product Management
    path('businesses/<int:business_id>/products/', views.product_list, name='product_list'),
    path('businesses/<int:business_id>/products/create/', views.product_create, name='product_create'),
    path('businesses/<int:business_id>/products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('businesses/<int:business_id>/products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('businesses/<int:business_id>/products/<int:product_id>/reviews', views.product_reviews, name='product_reviews'),
    
    # Sales Management
    path('businesses/<int:business_id>/sales/create/', views.create_sale, name='create_sale'),
    path('businesses/<int:business_id>/sales/history/', views.sales_history, name='sales_history'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]
