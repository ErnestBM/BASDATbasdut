from django.urls import path
from . import views
from CRUDPembuatanPertandingan.views import *

app_name = 'CRUDPembuatanPertandingan'

urlpatterns = [
    path('buatPertandingan/', views.buatPertandingan, name='buatPertandingan'),
    path('listStadium/', views.listStadium, name='listStadium'),
    path('listWaktu/', views.listWaktu , name='listWaktu'),
    path('listWasit/', views.listWasit, name='listWasit'),
    # path('delete-pertandingan/<int:pertandingan_id>/', views.delete_pertandingan, name='delete-pertandingan'),
]