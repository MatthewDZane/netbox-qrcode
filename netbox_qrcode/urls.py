from django.urls import path
from . import views

urlpatterns = [
    path('', views.QRcodeHomeView.as_view(), name='qrcodes'),
]