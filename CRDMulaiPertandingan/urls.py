from django.urls import path
from . import views
from .views import *

app_name = 'CRDMulaiPertandingan'

urlpatterns = [
    path('mulaiPertandingan/',views.mulaiPertandingan,name='mulaiPertandingan'),
    path('peristiwaTim/',views.peristiwaTim,name='peristiwaTim'),
]