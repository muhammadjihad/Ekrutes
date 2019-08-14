from django.urls import path, re_path
from . import views

app_name='akun-api'
urlpatterns = [
    path('login/',views.LoginAPIView.as_view(),name='login'),
    path('logout/',views.LogoutUserAPIView.as_view(),name='logout-api'),
    path('register/',views.RegisterAPIView.as_view(),name='register'),
    path('forgot-pass/',views.ForgotPasswordAPIView.as_view(),name='forgot-pass'),
    path('remember-login/',views.RememberLoginAPIView.as_view(),name='remember-login'),
    path('check-login/',views.CheckLogin.as_view(),name="check-login"),
    path('pilih-kota/',views.PilihKota.as_view(),name='pilih-kota'),
    path('pilih-kecamatan/',views.PilihKecamatan.as_view(),name='pilih-kecamatan'),
    re_path(r'^reset-pass/(?P<uidb64>[0-9A-Za-z_\-]+)/$',views.PasswordInputAPIView.as_view(), name='reset-pass'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]