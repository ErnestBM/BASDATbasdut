from django.urls import path
from .views import *
from authentication.views import logout

urlpatterns = [
    path('tipe-stadium', show_tipe_stadium, name='show_tipe_stadium'),
    path('waktu-stadium', show_waktu_stadium, name='show_waktu_stadium'),
    path('list-pertandingan/<str:tanggal>/<str:stadium>', show_list_pertandingan, name='list_pertandingan'),
    path('belitiket/<int:id_pertandingan>/', show_beli_tiket, name='show_beli_tiket'),
    path('logout', logout, name='logout')
]