from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('mulai/', show_mulai_rapat, name='show_mulai_rapat'),
    # path('isi_rapat/<uuid: uuid>/<str:teams>', show_isi_rapat, name='show_isi_rapat'),
]