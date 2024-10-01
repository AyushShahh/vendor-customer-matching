from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect(reverse("customer:home_page"))
        return render(request, 'vendor/index.html')
    return redirect(reverse('customer:landing_page'))
