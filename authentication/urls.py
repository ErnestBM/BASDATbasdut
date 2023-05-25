from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('', show_authentication, name='authentication'),
    path('register/', show_register, name='register'),
    path('register/panitia/', show_register_panitia, name='register_panitia'),
    path('register/lain/', show_register_lain, name='register_lain'),
    path('register/lain/submit/', register_lain, name='register_lain_submit'),
    path('register/panitia/submit/', register_panitia, name='register_panitia_submit'),
    path('logout/', logout, name='logout'),
]