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


class QRcodeDeviceView(View):
    template_name = 'netbox_qrcode/home.html'
    filterset_device = filters.SearchDeviceFilterSet

    def get(self, request):
        # Clear all objects in case of duplicate key violation
        QRExtendedDevice.objects.all().delete()
        
        base_url = request.build_absolute_uri('/') + 'media/image-attachments/'

        # Find all current Devices and instantiates new models that provide links to photos 
        for device in Device.objects.all().iterator():

            # Create device with resized url
            url_resized ='{}resized{}.png'.format(base_url, device.name)
            QRExtendedDevice.objects.get_or_create(name=device.name, id=device.id, device=device, status=device.status, device_role=device.device_role, device_type=device.device_type, site=device.site, rack=device.rack, photo='image-attachments/{}.png'.format(device.name), url=url_resized)

        # Create QuerySets from extended models
        queryset_device = QRExtendedDevice.objects.all()

        # Filter QuerySets
        queryset_device = self.filterset_device(request.GET, queryset_device).qs

        # Create Tables for each separate object's querysets
        table_device = QRDeviceTables(queryset_device)

        # Paginate Tables
        RequestConfig(request, paginate={"per_page": 50}).configure(table_device)

        # Render html with context
        return render(request, self.template_name, {
            'table_device': table_device, 
            'filter_form': forms.SearchFilterFormDevice(
                request.GET,
                label_suffix=''
            ),                
            })


class QRcodeRackView(View):
    template_name = 'netbox_qrcode/racks.html'
    filterset_rack = filters.SearchRackFilterSet

    def get(self, request):
        # Clear all objects in case of duplicate key violation
        QRExtendedRack.objects.all().delete()
        
        base_url = request.build_absolute_uri('/') + 'media/image-attachments/'

        # Find all current Racks and instantiates new models that provide links to photos 
        for rack in Rack.objects.all().iterator():

            # Create rack with resized url
            url_resized ='{}resized{}.png'.format(base_url, rack.name)
            QRExtendedRack.objects.get_or_create(name=rack.name, id=rack.id, rack=rack, facility_id=rack.facility_id, status=rack.status, site=rack.site, group=rack.group, role=rack.role, type=rack.type, photo='image-attachments/{}.png'.format(rack.name),url=url_resized)


        # Create QuerySets from extended models
        queryset_rack = QRExtendedRack.objects.all()

        # Filter QuerySets
        queryset_rack = self.filterset_rack(request.GET, queryset_rack).qs

        # Create Tables for each separate object's querysets
        table_rack = QRRackTables(queryset_rack)

        # Paginate Tables
        RequestConfig(request, paginate={"per_page": 25}).configure(table_rack)

        # Render html with context
        return render(request, self.template_name, {
            'table_rack': table_rack, 
            'filter_form': forms.SearchFilterFormRack(
                request.GET,
                label_suffix=''
            ),                
            })



class QRcodeCableView(View):
    template_name = 'netbox_qrcode/cables.html'
    filterset_cable = filters.SearchCableFilterSet

    def get(self, request):
        # Clear all objects in case of duplicate key violation
        QRExtendedCable.objects.all().delete()
        
        base_url = request.build_absolute_uri('/') + 'media/image-attachments/'

        # Find all current Cables and instantiates new models that provide links to photos 
        for cable in Cable.objects.all().iterator():

            # Create cable with resized url
            url_resized ='{}resized{}.png'.format(base_url, cable.name)
            QRExtendedCable.objects.get_or_create(name=cable.name, id=cable.id, cable=cable, _termination_a_device=cable._termination_a_device, _termination_b_device=cable._termination_b_device, photo='image-attachments/{}.png'.format(cable.name),url=url_resized)


        # Create QuerySets from extended models
        queryset_cable = QRExtendedCable.objects.all()

        # Filter QuerySets
        queryset_cable = self.filterset_cable(request.GET, queryset_cable).qs

        # Create Tables for each separate object's querysets
        table_cable = QRCableTables(queryset_cable)

        # Paginate Tables
        RequestConfig(request, paginate={"per_page": 25}).configure(table_cable)

        # Render html with context
        return render(request, self.template_name, {
            'table_cable': table_cable, 
            'filter_form': forms.SearchFilterFormCable(
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

        # Set images with or without text should be used and build url
        without_text = request.POST.get('without_text')

        # Print with text enabled
        if without_text is None:
            base_url = request.build_absolute_uri('/') + 'media/image-attachments/'

            # One image selected
            if image_count == 1:
                device = Model.objects.get(pk=pk_list[0])
                url = '{}{}.png'.format(base_url, device.name)
                image = Image.open(requests.get(url, stream=True).raw)

                context['image'] = get_img_b64(image)
                return render(request, self.template_name, context)

            # Multiple selected, account for multi page print
            elif image_count > 1:
                image_rows = []
                image_pages = []
                
                for i in range(0,image_count-1,2):

                    # First Image 
                    first_device = Model.objects.get(pk=pk_list[i])
                    first_url = '{}{}.png'.format(base_url, first_device.name)
                    first_image = Image.open(requests.get(first_url, stream=True).raw)
                    # Second Image
                    second_device = Model.objects.get(pk=pk_list[i+1])
                    second_url = '{}{}.png'.format(base_url, second_device.name)
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
                    url = '{}{}.png'.format(base_url, device.name)
                    image = Image.open(requests.get(url, stream=True).raw)
                    image_rows.append(image)

                final_image = image_rows[0]
                for i in range(1,len(image_rows)):
                    final_image = get_concat_v(final_image,image_rows[i])   

                # Convert and add as page
                image_pages.append(get_img_b64(final_image))

                # Send list of pages to print template
                context['image'] = image_pages

                # Insert template as context
                context['button_template'] = '''
                                            <button onclick="printImg({{image}})"; class="btn btn-xl btn-primary">
                                            <span class="glyphicon glyphicon-print" aria-hidden="true"></span>
                                            Print
                                            </button>
                                            '''

                return render(request, self.template_name, context)

            # No images selected, redirect to qrcode menu page
            else:
                return redirect('/plugins/netbox_qrcode/devices')
 
        # No text option selected
        else:
            base_url = request.build_absolute_uri('/') + 'media/image-attachments/noText'

            # One image selected
            if image_count == 1:
                device = Model.objects.get(pk=pk_list[0])
                url = '{}{}.png'.format(base_url, device.name)
                image = Image.open(requests.get(url, stream=True).raw)

                context['image'] = get_img_b64(image)
                return render(request, self.template_name, context)

            # Multiple selected, account for multi page print
            elif image_count > 1:
                image_curr = []
                image_rows = []
                image_rows_combined = []
                image_pages = []

                for i in range(image_count):

                    device = Model.objects.get(pk=pk_list[i])
                    url = '{}{}.png'.format(base_url, device.name)
                    image = Image.open(requests.get(url, stream=True).raw)
                    image_curr.append(image)

                    # If row full, push to row list and reset current
                    if ((i+1) % 6) == 0 and i > 0:
                        image_rows.append(image_curr)
                        image_curr = []
                    
                # Append row list with remaining images if any exists
                if image_curr:
                    # Make row an even count for print spacing
                    if len(image_curr) % 2 == 1:
                        image_curr.append(image_curr[0])
                    image_rows.append(image_curr)

                # Loop through each list of rows
                for row in image_rows:

                    # Combine images in single row into one image
                    first_image = row[0]
                    for i in range(1,len(row)):
                        first_image = get_concat(first_image,row[i])

                    image_rows_combined.append(first_image)

                # Combine rows into pages
                finished_page = image_rows_combined[0]
                i = 1

                while i < len(image_rows_combined):
                    finished_page = get_concat_v(finished_page,image_rows_combined[i])
                    i += 1

                    # If page full, push to page image and reset current
                    if (i % 8) == 0 and i > 0:
                        image_pages.append(get_img_b64(finished_page))
                        # If more rows to handle, setup next page image
                        if i < len(image_rows_combined):
                            finished_page = image_rows_combined[i]
                            i += 1
                
                image_pages.append(get_img_b64(finished_page))

                # Send list of pages to print template
                context['image'] = image_pages

                return render(request, self.template_name, context)
                
            # No images selected, redirect to qrcode menu page
            else:
                return redirect('/plugins/netbox_qrcode/devices')
