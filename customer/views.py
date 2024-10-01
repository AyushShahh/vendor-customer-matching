from django.shortcuts import render, redirect
from django.urls import reverse


def landing_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect(reverse("customer:home_page"))
        return redirect(reverse("vendor:index"))

    return render(request, 'customer/landing.html')


def home_page(request):
    if not request.user.is_authenticated:
        return redirect(reverse('customer:landing_page'))
    if request.user.user_type == 'vendor':
        return redirect(reverse("vendor:index"))
    return render(request, 'customer/index.html')
