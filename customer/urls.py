from django.urls import path
from . import views


app_name = 'customer'

urlpatterns = [
    path('', views.landing_view, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
    path('search/', views.search_view, name='search'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('watchlist/add/<int:product_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:product_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
]
