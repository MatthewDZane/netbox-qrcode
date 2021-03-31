from django.<a href="http" target="_blank">http</a> import HttpResponse
from django.urls import path
from . import views


def dummy_view(request):
    html = "<html><body>QRcode plugin</body></html>"
    return HttpResponse(html)

urlpatterns = [
    path('', dummy_view, name='qrcodes'),
]