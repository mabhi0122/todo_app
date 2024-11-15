from django.urls import path
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.custom_user, name= 'register'),
    path('login/', views.custom_login_view, name= 'login'),
    path('logout/', views.logout_user, name= 'logout'),

    path('request_reset_password/', views.request_reset_password, name="request_reset_password"),
    path('set_new_password/<uidb64>/<token>/', views.set_new_password, name= "set_new_password"),

    path('update-password/',views.password_change, name='update-password'),
    path('profile/', views.user_profile_view, name= 'profile'),
    path('update_user_profile/', views.update_user_profile, name= 'update_user_profile'),

    path('activate/<uidb64>/<token>/',views.account_activate, name= 'activate'),
]
