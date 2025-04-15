from django.urls import path
from . import views


urlpatterns = [
    path('login/<str:user_type>', views.login_view, name="login"),
    path('create/<str:user_type>', views.register, name="create"),
    path('profile', views.profile, name="profile"),
    path('edit-profile', views.edit_profile, name="edit_profile"),
    path('logout', views.logout_view, name="logout")
]
