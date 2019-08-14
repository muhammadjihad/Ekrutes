from django.urls import path,re_path
from . import views

app_name='superadmin-api'
urlpatterns = [ 
    path('',views.SuperAdminDashboardAPIView.as_view(),name='dashboard-view'),
    path('perusahaan-detail/',views.PerusahaanDetailAPIView.as_view(),name='perusahaan-detail'),
    path('token-input/',views.TokenDefaultAPIView.as_view(),name='token-input'),
    path('delete-hr/',views.DeleteHRAPIView.as_view(),name='delete-hr'),
    path('update-hr/',views.UpdateHRAPIView.as_view(),name='update-hr'),
    re_path(r'^upload-photo/(?P<id_foto>.+)$', views.UploadPhoto.as_view(),name='upload-photo'),
]