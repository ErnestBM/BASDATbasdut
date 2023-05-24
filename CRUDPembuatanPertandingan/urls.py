from django.urls import path
from CRUDPembuatanPertandingan.views import *

app_name = 'CRUDPembuatanPertandingan'

urlpatterns = [
    path('buat-pertandingan', show_buat_pertandingan, name='show_buat_pertandingan'),
    path('list-stadium', show_list_stadium, name='show_list_stadium'),
    path('list-waktu', show_list_waktu , name='show_list_waktu'),
    path('list-wasit', show_list_wasit, name='show_list_wasit')
]