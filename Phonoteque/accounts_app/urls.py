from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserLoginView, CustomPasswordChangeView, register, edit

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_page'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),

    # change password urls
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('profile/', profile_details, name="profile"),
    # path('profile/create/', create_profile_view, name="create profile"),
    # path('profile/edit/', edit_profile_view, name="edit profile"),
    # path('profile/delete/', delete_profile_view, name="delete profile"),
]
