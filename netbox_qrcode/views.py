from django.shortcuts import get_object_or_404, render
from django.views import View

class QRcodeHomeView(View):

    def get(self, request):
         return render(request,"netbox_qrcode/home.html")