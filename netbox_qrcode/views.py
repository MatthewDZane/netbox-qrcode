from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_tables2 import RequestConfig

from dcim.models import Device, Rack, Site, Cable
from dcim.tables import DeviceTable, RackTable, CableTable

from . import forms, filters

from .tables import QRDeviceTables, QRRackTables, QRCableTables
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable

from PIL import Image
from .utilities import get_img_b64, get_concat, get_concat_v
import requests


class QRcodeHomeView(View):
    template_name = 'netbox_qrcode/home.html'
    filterset_device = filters.SearchDeviceFilterSet
    filterset_rack = filters.SearchRackFilterSet
    filterset_cable = filters.SearchCableFilterSet

    def get(self, request):
        # Clear all objects in case of duplicate key violation
        QRExtendedDevice.objects.all().delete()
        QRExtendedRack.objects.all().delete()
        QRExtendedCable.objects.all().delete()

        # Find all current Devices, Racks, Cables and instantiates new models that provide links to photos 
        for device in Device.objects.all().iterator():

            # Create device with resized url
            url_resized ='https://netbox.nrp-nautilus.io/media/image-attachments/resized{}.png'.format(device.name)
            QRExtendedDevice.objects.get_or_create(name=device.name, id=device.id, device=device, status=device.status, device_role=device.device_role, device_type=device.device_type, site=device.site, rack=device.rack, photo='image-attachments/{}.png'.format(device.name), url=url_resized)
            
        for rack in Rack.objects.all().iterator():

            # Create rack with resized url
            url_resized ='https://netbox.nrp-nautilus.io/media/image-attachments/resized{}.png'.format(rack.name)
            QRExtendedRack.objects.get_or_create(name=rack.name, id=rack.id, rack=rack, status=rack.status, site=rack.site, group=rack.group, role=rack.role, photo='image-attachments/{}.png'.format(rack.name),url=url_resized)

        for cable in Cable.objects.all().iterator():

            # Create cable with resized url
            url_resized ='https://netbox.nrp-nautilus.io/media/image-attachments/resized{}.png'.format(cable.name)
            QRExtendedCable.objects.get_or_create(name=cable.name, id=cable.id, cable=cable, photo='image-attachments/{}.png'.format(cable.name),url=url_resized)


        # Create QuerySets from extended models
        queryset_device = QRExtendedDevice.objects.all()
        queryset_rack = QRExtendedRack.objects.all()
        queryset_cable = QRExtendedCable.objects.all()

        # Filter QuerySets
        queryset_device = self.filterset_device(request.GET, queryset_device).qs
        queryset_rack = self.filterset_rack(request.GET, queryset_rack).qs
        queryset_cable = self.filterset_cable(request.GET, queryset_cable).qs


        # Create Tables for each separate object's querysets
        table_device = QRDeviceTables(queryset_device)
        table_rack = QRRackTables(queryset_rack)
        table_cable = QRCableTables(queryset_cable)

        # Paginate Tables
        RequestConfig(request, paginate={"per_page": 25}).configure(table_device)
        RequestConfig(request, paginate={"per_page": 25}).configure(table_rack)
        RequestConfig(request, paginate={"per_page": 25}).configure(table_cable)

        # Render html with context
        return render(request, self.template_name, {
            'table_device': table_device, 
            'table_rack': table_rack, 
            'table_cable': table_cable, 
            'filter_form': forms.SearchFilterFormDevice(
                request.GET,
                label_suffix=''
            ),                
            })



# View for when 'Print Selected' Button Pressed
class PrintView(View):

    template_name = 'netbox_qrcode/print.html'

    # Collect post form content from menu page
    def post(self, request):

        context = {}
        pk_list = request.POST.getlist('pk')

        # Get type of netbox object being printed
        name = request.POST.get('obj_type')
        context['name'] = name

        # Switch model based on object type
        obj_dict = {"Devices": Device , "Racks": Rack, "Cables": Cable}
        Model = obj_dict[name]


        # Switch table based on object type
        table_dict = {"Devices": DeviceTable, "Racks": RackTable, "Cables": CableTable}
        object_queryset = Model.objects.filter(pk__in=pk_list)
        context['table'] = table_dict[name](object_queryset)

        # Number of Images Selected to print
        image_count = len(pk_list)

        # One image selected
        if image_count == 1:
            device = Model.objects.get(pk=pk_list[0])
            url = 'https://netbox.nrp-nautilus.io/media/image-attachments/{}.png'.format(device.name)
            image = Image.open(requests.get(url, stream=True).raw)

            context['image'] = get_img_b64(image)
            return render(request, self.template_name, context)

        # Multiple selected, account for multi page print
        elif image_count > 1:
            image_rows = []
            image_pages = []
            
            for i in range(0,len(pk_list)-1,2):

                # First Image 
                first_device = Model.objects.get(pk=pk_list[i])
                first_url = 'https://netbox.nrp-nautilus.io/media/image-attachments/{}.png'.format(first_device.name)
                first_image = Image.open(requests.get(first_url, stream=True).raw)
                # Second Image
                second_device = Model.objects.get(pk=pk_list[i+1])
                second_url = 'https://netbox.nrp-nautilus.io/media/image-attachments/{}.png'.format(second_device.name)
                second_image = Image.open(requests.get(second_url, stream=True).raw)
                # Create image row and add to list
                row = get_concat(first_image,second_image)
                image_rows.append(row)

                # If full page made, add as separate print page and clear current rows
                if (i % 10) == 8 and i > 0:
                    final_image = image_rows[0]
                    for i in range(1,len(image_rows)):
                        final_image = get_concat_v(final_image,image_rows[i])   
                    image_pages.append(get_img_b64(final_image))
                    image_rows = []

            # If odd image count, add single image as row
            if image_count % 2 == 1:
                device = Model.objects.get(pk=pk_list[image_count-1])
                url = 'https://netbox.nrp-nautilus.io/media/image-attachments/{}.png'.format(device.name)
                image = Image.open(requests.get(url, stream=True).raw)
                image_rows.append(image)

            final_image = image_rows[0]
            for i in range(1,len(image_rows)):
                final_image = get_concat_v(final_image,image_rows[i])   

            # Convert and add as page
            image_pages.append(get_img_b64(final_image))

            # Send list of pages to print template
            context['image'] = image_pages
            return render(request, self.template_name, context)

        # No images selected, redirect to qrcode menu page
        else:
            return redirect('/plugins/netbox_qrcode')
