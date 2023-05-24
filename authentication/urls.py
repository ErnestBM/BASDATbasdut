from django.contrib import admin
from django.urls import path
from .views import *



urlpatterns = [
    path('login', show_authentication, name='authentication'),
    # path('login', show_login, name='show_login'),
    path('', login, name='login'),
    path('register', show_register, name='register'),
    path('register/panitia', show_register_panitia, name='register_panitia'),
    path('register/lain', show_register_lain, name='register_lain'),
    path('logout', logout, name='logout'),
]