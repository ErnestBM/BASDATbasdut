from django.urls import path
from . import views
from .views import *

app_name = 'RManagePertandingan'

urlpatterns = [
    path('managePertandingan/',views.managePertandingan,name='managePertandingan'),
    path('createNextPertandingan/',views.createNextPertandingan,name='createNextPertandingan'),
    path('endPertandingan/',views.endPertandingan,name='endPertandingan'),
    path('updatePertandingan/',views.updatePertandingan,name='updatePertandingan'),
    path('panggilPeristiwa/<str : id>',views.panggilPeristiwa,name='panggilPeristiwa'),
]
