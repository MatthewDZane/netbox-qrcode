from django.shortcuts import get_object_or_404, render
from django.views import View
from dcim.models import Cable, Device, Interface, DeviceRole
from . import forms, filters

# class QRcodeHomeView(View):

#     def get(self, request):
#          return render(request,"netbox_qrcode/home.html")

class QRcodeHomeView(View):
    queryset = Device.objects.all()
    # filterset = filters.SearchFilterSet
    template_name = 'netbox_qrcode/home.html'

    def get(self, request):

        # if not request.GET:
        #     self.queryset = Device.objects.none()

        # layout_context = {}

        # self.queryset = self.filterset(request.GET, self.queryset).qs

        return render(request, self.template_name)