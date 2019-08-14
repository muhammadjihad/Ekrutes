from django.urls import path
from . import views

app_name='peserta-api'
urlpatterns = [
    path('register/',views.RegistrasiPesertaAPI.as_view(),name='register')
]