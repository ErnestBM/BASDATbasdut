from django.contrib import admin
from django.urls import path
from authentication.views import *


urlpatterns = [
    path('', show_login, name='show_login'),
    path('login', login, name='login')
]