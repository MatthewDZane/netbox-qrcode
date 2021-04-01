from django.urls import path
from . import views

urlpatterns = [
    path('qrcodes/', views.QRcodeHomeView.as_view(), name='qrcodes'),
]