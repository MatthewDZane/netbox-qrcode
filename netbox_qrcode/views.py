import requests

from django.shortcuts import redirect, render
from django.views import View
from django_tables2 import RequestConfig

from dcim.models import Device, Rack, Cable
from dcim.tables import DeviceTable, RackTable, CableTable

from . import forms, filters

from .tables import QRDeviceTables, QRRackTables, QRCableTables
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable

from PIL import Image
from .utilities import *

from django.conf import settings

import threading


class QRcodeDeviceView(View):
    template_name = 'netbox_qrcode/devices.html'
    filterset_device = filters.SearchDeviceFilterSet

    def get(self, request):
        # Create QuerySets from extended models
        queryset_device = QRExtendedDevice.objects.all()

        # Filter QuerySets
        queryset_device = self.filterset_device(
            request.GET, queryset_device).qs

        # Create Tables for each separate object's querysets
        table_device = QRDeviceTables(queryset_device)

        # Render html with context
        return render(request, self.template_name, {
            'table_device': table_device,
            'filter_form': forms.SearchFilterFormDevice(
                request.GET,
                label_suffix=''
            ),
        })

    def post(self, request):

        # Get slider values
        font_size = request.POST.get('font-size-range')
        box_size = request.POST.get('box-size-range')
        border_size = request.POST.get('border-size-range')

        # Reload all Object QR Images with input parameters
        numReloaded = reloadQRImages(request, Device, "devices", int(
            font_size), int(box_size), int(border_size))

        # Create QuerySets from extended models
        queryset_device = QRExtendedDevice.objects.all()

        # Filter QuerySets
        queryset_device = self.filterset_device(
            request.GET, queryset_device).qs

        # Create Tables for each separate object's querysets
        table_device = QRDeviceTables(queryset_device)

        # Paginate Tables
        #RequestConfig(request, paginate={
        #              "per_page": 50}).configure(table_device)

        # Render html with context
        return render(request, self.template_name, {
            'table_device': table_device,
            'filter_form': forms.SearchFilterFormDevice(
                request.GET,
                label_suffix=''
            ),
            'successMessage': '<div class="text-center text-success" style="padding-top: 10px">Successfully Reloaded {} Devices</div>'.format(numReloaded),
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
            url_resized = '{}resized{}.png'.format(base_url, rack._meta.object_name + str(rack.pk))
            QRExtendedRack.objects.get_or_create(
                id=rack.id,
                rack=rack,
                name=rack.name,
                status=rack.status,
                site=rack.site,
                role=rack.role,
                photo='image-attachments/{}.png'.format(rack._meta.object_name + str(rack.pk)),
                url=url_resized
            )

        # Create QuerySets from extended models
        queryset_rack = QRExtendedRack.objects.all()

        # Filter QuerySets
        queryset_rack = self.filterset_rack(request.GET, queryset_rack).qs

        # Create Tables for each separate object's querysets
        table_rack = QRRackTables(queryset_rack)

        # Paginate Tables
        RequestConfig(request, paginate={"per_page": 50}).configure(table_rack)

        # Render html with context
        return render(request, self.template_name, {
            'table_rack': table_rack,
            'filter_form': forms.SearchFilterFormRack(
                request.GET,
                label_suffix=''
            ),
        })

    def post(self, request):
        # Get slider values
        font_size = request.POST.get('font-size-range')
        box_size = request.POST.get('box-size-range')
        border_size = request.POST.get('border-size-range')

        # Reload all Object QR Images
        numReloaded = reloadQRImages(request, Rack, "racks", int(
            font_size), int(box_size), int(border_size))

        # Create QuerySets from extended models
        queryset_rack = QRExtendedRack.objects.all()

        # Filter QuerySets
        queryset_rack = self.filterset_rack(request.GET, queryset_rack).qs

        # Create Tables for each separate object's querysets
        table_rack = QRRackTables(queryset_rack)

        # Paginate Tables
        RequestConfig(request, paginate={"per_page": 50}).configure(table_rack)

        return render(request, self.template_name, {
            'table_rack': table_rack,
            'filter_form': forms.SearchFilterFormRack(
                request.GET,
                label_suffix=''
            ),
            'successMessage': '<div class="text-center text-success" style="padding-top: 10px">Successfully Reloaded {} Racks</div>'.format(numReloaded),
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
            url_resized = '{}resized{}.png'.format(base_url, cable._meta.object_name + str(cable.pk))
            QRExtendedCable.objects.get_or_create(
                id=cable.id,
                cable=cable,
                name=cable._meta.object_name + str(cable.pk),
                photo='image-attachments/{}.png'.format(cable._meta.object_name + str(cable.pk)),
                url=url_resized
            )

        # Create QuerySets from extended models
        queryset_cable = QRExtendedCable.objects.all()

        # Filter QuerySets
        queryset_cable = self.filterset_cable(request.GET, queryset_cable).qs

        # Create Tables for each separate object's querysets
        table_cable = QRCableTables(queryset_cable)

        # Paginate Tables
        RequestConfig(request, paginate={
                      "per_page": 50}).configure(table_cable)

        # Render html with context
        return render(request, self.template_name, {
            'table_cable': table_cable,
            'filter_form': forms.SearchFilterFormCable(
                request.GET,
                label_suffix=''
            ),
        })

    def post(self, request):
        # Get slider values
        font_size = request.POST.get('font-size-range')
        box_size = request.POST.get('box-size-range')
        border_size = request.POST.get('border-size-range')

        # Reload all Object QR Images
        numReloaded = reloadQRImages(request, Cable, "cables", int(
            font_size), int(box_size), int(border_size))

        # Create QuerySets from extended models
        queryset_cable = QRExtendedCable.objects.all()

        # Filter QuerySets
        queryset_cable = self.filterset_cable(request.GET, queryset_cable).qs

        # Create Tables for each separate object's querysets
        table_cable = QRCableTables(queryset_cable)

        # Paginate Tables
        RequestConfig(request, paginate={
                      "per_page": 50}).configure(table_cable)

        # Render html with context
        return render(request, self.template_name, {
            'table_cable': table_cable,
            'filter_form': forms.SearchFilterFormCable(
                request.GET,
                label_suffix=''
            ),
            'successMessage': '<div class="text-center text-success" style="padding-top: 10px">Successfully Reloaded {} Cables</div>'.format(numReloaded),
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
        obj_dict = {"Devices": Device, "Racks": Rack, "Cables": Cable}
        Model = obj_dict[name]

        # Switch table based on object type
        table_dict = {"Devices": DeviceTable,
                      "Racks": RackTable, "Cables": CableTable}
        object_queryset = Model.objects.filter(pk__in=pk_list)
        context['table'] = table_dict[name](object_queryset)

        # Number of Images Selected to print
        image_count = len(pk_list)

        # Set images with or without text should be used and build url
        without_text = request.POST.get('without_text')

        def combine_rows(imageRow, numRows):
            """
            Concatenates rows into pages
            :param imageRow: List of rows of images
            :param numRows: Number of rows in a page
            :return: List of pages of images
            """

            image_pages = []

            final_image = imageRow[0]
            i = 1

            while i < len(imageRow):
                final_image = get_concat_v(final_image, imageRow[i])
                i += 1

                # If page full, push to page image and reset current
                if (i % numRows) == 0 and i > 0:
                    image_pages.append(get_img_b64(final_image))
                    # If more rows to handle, setup next page image
                    if i < len(imageRow):
                        final_image = imageRow[i]
                        i += 1

            if i % numRows != 0:
                # Convert and add as page
                image_pages.append(get_img_b64(final_image))

            return image_pages

        # No text setting option selected
        if without_text:
            base_url = request.build_absolute_uri(
                '/') + 'media/image-attachments/noText'
            rowSize = 6
            numRows = 8
            horizontal_print_padding = 40
            footer_text_height = 20
            text_padding = 10
            context['without_text'] = 1
        # Print with text enabled and with below settings
        else:
            base_url = request.build_absolute_uri(
                '/') + 'media/image-attachments/'
            rowSize = 3
            numRows = 10
            horizontal_print_padding = 110
            vertical_print_padding = 5
            context['without_text'] = 0

        # Multiple selected, account for multi page print
        if image_count > 0:
            image_curr = []
            image_rows = []
            image_rows_combined = []
            for i in range(image_count):

                obj = Model.objects.get(pk=pk_list[i])
                url = '{}{}.png'.format(base_url, obj._meta.object_name + str(obj.pk))
                try:
                    image = Image.open(requests.get(url, stream=True).raw)
                # UnidentifiedImageError, NameError
                except:
                    image = Image.new('L', (100,100), 'white')
                    
                # Append info to bottom of image using user config font if no text QR
                obj_name = obj.name if hasattr(obj, 'name') else obj._meta.object_name + str(obj.pk)
                if without_text:
                    text_img = get_qr_text((image.width, footer_text_height), obj_name, settings.PLUGINS_CONFIG.get(
                        'netbox_qrcode', {}).get('font'), 200)
                    text_img = add_print_padding_v(text_img, text_padding)
                    image = get_concat_v(image, text_img)

                # Resize text Qr and add vertical padding
                else:
                    resize_width_height = (162, 88)
                    image = image.resize(resize_width_height)
                    image = add_print_padding_v(image, vertical_print_padding)

                # Append modified image
                image_curr.append(image)

                # If row full, push to row list and reset current
                if ((i+1) % rowSize) == 0:
                    image_rows.append(image_curr)
                    image_curr = []

            # Append row list with remaining images if any exists
            if image_curr:
                # Make row full for print spacing
                for i in range(0, rowSize-len(image_curr)):
                    blank = Image.new('L', image.size, 'white')
                    image_curr.append(blank)
                image_rows.append(image_curr)

            # Loop through each list of rows
            for row in image_rows:

                # Combine images in single row into one image
                first_image = row[0]
                for i in range(1, len(row)):
                    # Add left side padding to all but first image in row and append
                    row[i] = add_print_padding_left(row[i], horizontal_print_padding)
                    first_image = get_concat(first_image, row[i])

                image_rows_combined.append(first_image)

            # Send list of pages to print template
            context['image'] = combine_rows(image_rows_combined, numRows)

            return render(request, self.template_name, context)

        # No images selected, split current path to remove /print and redirect back to respective object page
        else:
            return redirect('/'.join(self.request.path_info.split('/')[:-2]))


class ReloadQRThread(threading.Thread):
    def __init__(self, objects, object_name, font_size, box_size, border_size, force_reload_all):
        threading.Thread.__init__(self)
        self.objects = objects
        self.object_name = object_name
        self.font_size = font_size
        self.box_size = box_size
        self.border_size = border_size
        self.force_reload_all = force_reload_all

    def run(self):
        threadLock.acquire()
        self.reload_qr_images()
        threadLock.release()

    def reload_qr_images(self):
        if force_reload_all:
            for obj in self.objects:
                numReloaded += 1
                reload_qr_image(obj)
        else:
            for obj in self.objects:
                # Check if qrcode already exists
                image_url = request.build_absolute_uri(
                    '/') + 'media/image-attachments/{}.png'.format(obj._meta.object_name + str(obj.pk))
                rq = requests.get(image_url)

                # Create QR Code only for non-existing or if forced
                if rq.status_code != 200:
                    numReloaded += 1
                    reload_qr_image(obj)

    def reload_qr_image(self, obj):
        url = request.build_absolute_uri(
            '/') + 'dcim/{}/{}'.format(self.object_name, obj.pk)

        # Get object config settings
        obj_cfg = config.get(self.object_name[:-1])
        if obj_cfg is None:
            return ''
        # and override default config
        config.update(obj_cfg)

        # Override User Config with print settings
        printConfig = {}
        printConfig['qr_box_size'] = self.box_size
        printConfig['qr_border'] = self.border_size

        config.update(printConfig)

        qr_args = {}
        for k, v in config.items():
            if k.startswith('qr_'):
                qr_args[k.replace('qr_', '')] = v

        # Create qr image
        qr_img = get_qr(url, **qr_args)

        # Handle qr text if enabled
        if config.get('with_text'):
            text = []
            for text_field in config.get('text_fields', []):
                cfn = None
                if '.' in text_field:
                    try:
                        text_field, cfn = text_field.split('.')
                    except ValueError:
                        cfn = None
                if getattr(obj, text_field, None):
                    if cfn:
                        try:
                            if getattr(obj, text_field).get(cfn):
                                text.append('{}'.format(
                                    getattr(obj, text_field).get(cfn)))
                        except AttributeError:
                            pass
                    else:
                        text.append('{}'.format(getattr(obj, text_field)))
            custom_text = config.get('custom_text')
            if custom_text:
                text.append(custom_text)
            text = '\n'.join(text)

            # Create qr text with image size and text
            text_img = get_qr_text(
                qr_img.size, text, config.get('font'), self.font_size)

            # Combine qr image and qr text
            qr_with_text = get_concat(qr_img, text_img)

            # Save image with text to container with object's first field name
            text_fields = config.get('text_fields', [])
            file_path = '/opt/netbox/netbox/media/image-attachments/{}.png'.format(
                obj._meta.object_name + str(obj.pk))
            qr_with_text.save(file_path)

            # Save image without text to container
            file_path = '/opt/netbox/netbox/media/image-attachments/noText{}.png'.format(
                obj._meta.object_name + str(obj.pk))
            resize_width_height = (90, 90)
            qr_img = qr_img.resize(resize_width_height)
            qr_img.save(file_path)

            # Resize final image for thumbnails and save
            resize_width_height = (120, 50)
            qr_with_text = qr_with_text.resize(resize_width_height)
            file_path = '/opt/netbox/netbox/media/image-attachments/resized{}.png'.format(
                obj._meta.object_name + str(obj.pk))
            qr_with_text.save(file_path)

def reloadQRImages(request, Model, objName, font_size=100, box_size=3, border_size=0):
    """
    Creates QRcode image with text, without text, and thumbsized for netbox objects and saves to disk 
    :param request: network request
    :param Model: netbox object
    :param objName:  netbox object string name
    :return: number of object images created
    """

    # Collect User Config and make copy
    config = settings.PLUGINS_CONFIG.get('netbox_qrcode', {}).copy()

    threads = []
    numReloaded = 0
    objects = Model.objects.all().iterator()
    force_reload_all = request.POST.get('force-reload-all')
    threads.append(ReloadQRThread(split_objects(objects, 5), objName, font_size, box_size, border_size), force_reload_all)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return numReloaded


def split_objects(objects, num_chunks):
    """Yield successive n-sized chunks from lst."""
    chunk_size = objects / num_chunks
    for i in range(0, len(objects), chunk_size):
        yield objects[i:i + chunk_size]