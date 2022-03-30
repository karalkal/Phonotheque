from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserLoginView, CustomPasswordChangeView, register, edit, ProfileDetailView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_page'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile_details'),

    # change password urls
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),


]
