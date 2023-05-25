from .views import *
from django.urls import path
from authentication.views import logout


urlpatterns = [
    path('list_rapat', show_list_rapat, name='show_list_rapat'),
    path('lihat_hasil_rapat/<int:id_pertandingan>', show_hasil_rapat, name='show_hasil_rapat'),
    path('logout', logout, name='logout'),
]