from django.urls import path, include
from .views import UserView, UserDetails, reset_pass_code_api, reset_pass_api
from rest_framework import routers
from rest_framework.authtoken import views


urlpatterns = [
    path('', UserView, name='url_account'),
    path('<int:pk>/', UserDetails.as_view(), name='UserDetails'),
    path('token/', views.obtain_auth_token),
    path('password-reset-code/', reset_pass_code_api, name='code_pass'),
    path('password-reset/', reset_pass_api, name='code_pass'),
]
