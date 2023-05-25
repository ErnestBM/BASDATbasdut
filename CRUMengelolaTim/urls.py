from django.urls import path
from CRUMengelolaTim.views import *

app_name = "CRUMengelolaTim"

urlpatterns = [
    path('', show_dashboard_manajer, name="dashboard_manajer"),
    path('regist_tim/', show_tim_form, name="register_tim"),
    path('timdetail/', get_pemain_pelatih, name='tim_detail'),
    path('regist-tim/submit', register_tim, name="register_tim_submit"),
]
