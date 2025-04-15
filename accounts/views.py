from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from . models import CustomUser, Customer, Vendor
from django.http import HttpResponse
from django.contrib import messages


def login_view(request, user_type):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect(reverse("customer:home_page"))
        return redirect(reverse("vendor:index"))
    elif user_type in ['customer', 'vendor']:
        if request.method == 'GET':
            return render(request, 'accounts/auth.html', {
                'user_type': user_type,
                'action': 'login'
            })

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user_type == 'customer':
                return redirect(reverse("customer:home_page"))
            return redirect(reverse("vendor:index"))
        else:
            return render(request, 'accounts/auth.html', {
                'user_type': user_type,
                'message': 'Invalid email or password.',
                'action': 'login'
            })

    return redirect(reverse('customer:landing_page'))


def register(request, user_type):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect(reverse("customer:home_page"))
        return redirect(reverse("vendor:index"))
    elif user_type in ['vendor', 'customer']:
        if request.method == 'GET':
            return render(request, 'accounts/auth.html', {
                'user_type': user_type,
                'action': 'register'
            })

        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmation')
        city = request.POST.get('city')
        area = request.POST.get('area')
        state = request.POST.get('state')
        phone_number = request.POST.get('number')
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')

        if password != confirm_password:
            return render(request, 'accounts/auth.html', {
                'user_type': user_type,
                'action': 'register',
                'message': 'Passwords do not match'
            })

        try:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                user_type=user_type,
                city=city,
                area=area,
                state=state,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name
            )

            if user_type == 'customer':
                Customer.objects.create(user=user)
            elif user_type == 'vendor':
                Vendor.objects.create(user=user)

            login(request, user)
            if user_type == 'customer':
                return redirect(reverse("customer:home_page"))
            return redirect(reverse("vendor:index"))
        except Exception as e:
            return render(request, 'accounts/auth.html', {
                'user_type': user_type,
                'action': 'register',
                'message': f"{str(e)}"
            })

    return redirect(reverse('customer:landing_page'))


def profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse('customer:landing_page'))
    return render(request, 'accounts/profile.html')


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse('customer:landing_page'))
    user = request.user
    error_message = None
    if request.method == 'POST':
        try:
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.area = request.POST.get('area', user.area)
            user.city = request.POST.get('city', user.city)
            user.state = request.POST.get('state', user.state)
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        except Exception as e:
            error_message = str(e)
    return render(request, 'accounts/edit_profile.html', {'error_message': error_message})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('customer:landing_page'))
    return HttpResponse(status=403)

