from django.urls import path
from . import views

urlpatterns = [
    path('qrcode/', views.QRcodeHomeView.as_view(), name='qrcodes'),
]