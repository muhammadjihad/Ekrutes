from django.urls import path, re_path
from . import views

app_name='akun-api'
urlpatterns = [
    path('login/',views.LoginAPIView.as_view(),name='login'),
    path('register/',views.RegisterAPIView.as_view(),name='logout'),
    path('forgot-pass/',views.ForgotPasswordAPIView.as_view(),name='forgot-pass'),
    path('remember-login/',views.RememberLoginAPIView.as_view(),name='remember-login'),
    re_path(r'^reset-pass/(?P<uidb64>[0-9A-Za-z_\-]+)/$',views.PasswordInputAPIView.as_view(), name='activate'),
]