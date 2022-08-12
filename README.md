# Netbox QR Code Plugin

[Netbox](https://github.com/netbox-community/netbox) plugin for generate QR codes for objects: Device, Rack, Cable, Location

Created by Jason Lin and Maintained by [Matthew Zane](https://github.com/MatthewDZane/)

This plugin depends on [qrcode](https://github.com/lincolnloop/python-qrcode) and [Pillow](https://github.com/python-pillow/Pillow) python library

## Compatibility

This plugin in compatible with [NetBox](https://netbox.readthedocs.org/) 3.10 and later.

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

```
pip install netbox-qrcode
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_qrcode']
```
Restart NetBox and add `netbox-qrcode` to your local_requirements.txt

## Configuration

The following options are available:

* `with_text`: Boolean (default True). Text label will be added to QR code image if enabled.
* `text_fields`: List of String (default ['name']). Text fields of an object that will be added as text label to QR image. It's possible to use custom field values.
* `font`: String (default TahomaBold) Font name for text label ( Some font include in package, see fonts dir).
* `text_location`: Where to render the text, relative to the QR code.  Valid values are `"right"` (default), `"left"`", `"up"`, and `"down"`.
* `custom_text`: String or None (default None) additional text label to QR code image (will be added after text_fields).
* `qr_version`: Integer (default 1) parameter is an integer from 1 to 40 that controls the size of
the QR Code (the smallest, version 1, is a 21x21 matrix).
* `qr_error_correction`: Integer (default 0),  controls the error correction used for the
QR Code. The following values are available:

   1 - About 7% or less errors can be corrected.
   0 - About 15% or less errors can be corrected.
   2 - About 30% or less errors can be corrected.
   3 - About 25% or less errors can be corrected.

* `qr_box_size`: Integer (default 6),  controls how many pixels each "box" of the QR code
is.
* `qr_border`: Integer (default 4),  controls how many boxes thick the border should be
(the default is 4, which is the minimum according to the specs).

### Per object options

Per object options override default options. Per object options dictionary can contains any of default options inside.

* `device`: Dict or None (default {'text_fields': ['name', 'serial']}), set None to disble QR code
* `rack`: Dict or None (default {'text_fields': ['name']}), set None to disble QR code
* `cable`: Dict or None (default {'text_fields': ['_termination_a_device', 'termination_a', '_termination_b_device', 'termination_b',]}), set None to disble QR code
* `location`: Dict or None (default {'text_fields': ['name']}), set None to disble QR code

Configuration example:
```
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        'with_text': True,
        'text_fields': ['name', 'serial'],
        'font': 'ArialMT',
        'custom_text': 'Property of SomeCompany\ntel.8.800333554-CALL',
        'text_location': 'up',
        'qr_version': 1,
        'qr_error_correction': 0,
        'qr_box_size': 4,
        'qr_border': 4,
        # per object options
        'device': {
            'qr_box_size': 6,
            'custom_text': None,
        },
        'rack': {
            'text_fields': [
                'site',
                'name',
                'facility_id',
                'tenant',
                'cf.cf_name'
            ]
        },
        'cable': None,  # disable QR code for Cable object
        'location': {
            'text_fields': ['name']
        }
    }
}
```

## Pages
The following are the available pages in the plugin
```
- plugins/netbox_qrcode/
    - devices/
        - print/
    - racks/
        - print/
    - cables/
        - print/
    - locations/
        - print/
```
The URL of each page is defined in [netbox_qrcode/urls.py](netbox_qrcode/urls.py).
```
# netbox_qrcode/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.QRcodeDeviceView.as_view(), name='qrcode_devices'),
    path('racks/', views.QRcodeRackView.as_view(), name='qrcode_racks'),
    path('cables/', views.QRcodeCableView.as_view(), name='qrcode_cables'),
    path('locations/', views.QRcodeLocationView.as_view(), name='qrcode_locations'),

    path('devices/print/', views.PrintView.as_view(), name='print_menu'),
    path('racks/print/', views.PrintView.as_view(), name='print_menu'),
    path('cables/print/', views.PrintView.as_view(), name='print_menu'),
    path('locations/print/', views.PrintView.as_view(), name='print_menu'),
]
```
The urlpatterns variable holds all the paths in the plugin. Each path references a django.views.View. 

## Views
Custom Views are defined in [netbox_qrcode/views.py](netbox_qrcode/views.py)

### Model Views
```
# views.py
# import django and netbox modules
...
class QRcodeDeviceView(View):
    ...

    def get(self, request):
        ...

    def post(self, request):
        ...

class QRcodeRackView(View):
    ...

class QRcodeCableView(View):
    ...

class QRcodeLocationView(View):
    ...
```
Each of these views define a "get" and a "post" function, which handle their respective requests for the given view. You can add more functions for the other request types in these classes.

#### GET
A GET request is performed simply by loading the page in a browser. It will load and display all previously generated Netbox QRCode Extended objects, which are defined in [netbox_qrcode/models.py](netbox_qrcode/models.py). The objects are displayed in a table similar to the standard Netbox tables. Note: This will not necessary display the most update data (see [POST](#post)).

#### POST
A POST request is performed by clicking the "Reload QR Codes" button or "Reload Objects" button. Each button will perform the corresponding operation in the NetBox instance, by setting the request head with the corresponding key-value pair.


### PrintView
```
# View for when 'Print Selected' Button Pressed
class PrintView(View):
    ...

    def post(self, request):
        ...

class ReloadQRThread(threading.Thread):
    ...
    def run(self):
        ...

    def join(self):
        ...

    def reload_qr_image(self, obj):
        ...

def reloadQRImages(request, Model, objName, font_size=100, box_size=3, border_size=0):
    ...
```
The PrintView view is accessed via the "Print Selected" button on the Model Views. This simply takes the user to a view of the chosen QR Codes to be printed.

## How to Use

### Update Plugin Objects
The "Reload Objects" button will perform an operation which updates all of the Plugin models, in the corresponding view, with the data stored in the NetBox database so that the plugin objects have a one-to-one relationship with the base NetBox objects.
- New object are created for new base NetBox objects
- Existing plugin objects are updated
- Plugin objects which no longer have an existing base NetBox object counterpart are deleted

Note: This function was originally included in the GET request, so the plugin objects would always be updated upon loading a page, but if there is a large volume of entries, the page may timeout before completing, causing the page to be in accessable. Moving it into the POST request allows the GET request to always load. So, the "Reload Objects" button may cause the page to timeout, but the user can just simply reload the page and wait, beacuse the operation will continue after timingout.

### Generating QR Codes
The "Reload QR Codes" button will Create/Update QR Codes for the chosen objects, using the settings defined by the sliders. 
There are 4 slider settings:
1) Font Size - the size of the font of the text
2) Box Size - the size of the QR Code image
3) Border Size - the size of the border between the QR Code and the edges of the image
4) Max Line Length -  the maximum length of each line of the text. Text will wrap if it exceeds the specified value

Objects to Reload QR Code for are selected by checking the box of the corresponding entry in the table. Logic is applied in the following order:
1) If the "Force Reload All" checkbox is ticked, then all objects will be reloaded.
2) If at least one object is chosen, only the chosen object will be reloaded.
3) If no objects are chosen, only objects which do not have a QR Code image will be reloaded.

Note: Like the "Reload Objects" button, this may cause the page to timeout, but the operation will continue. 

### Printing QR Codes
There are two ways of printing QR Codes: 
1) Individually from the base NetBox individual view (Devices, Racks, Cables, or Locations)
- For example, on dcim/devices/123, toward the bottom of the page there is a QR Code image displayed and a "Print" button
- Print one QR Code for the specific object
- Prints the exact QR Code generated from the plugins pages
2) 1 or more objects in a format for an Avery Lable template.
- For example, select one or more locations, on netbox_qrcode/locations, click "Print Selected". This will take the user to netbox_qrcode/locations/print which displays the image(s) to print and a "Print" button.
- Takes all of the QR Codes for the selected objects and compiles them into rows and columns on page sized image(s), with each QR Code a set size for the Avery template.


### ReloadQRThread
This class is used to run multiple threads to generate the QR Codes faster. Here is some additional information on [threads](https://www.pythontutorial.net/python-concurrency/python-threading/). Note: This was implemented as a solution to the POST requests timing out, but it may be that the QR Code Extended object update process takes too long. 

## Models
The NetBox QR Code plugin adds for new models: QRExtendedDevice, QRExtendedRack, QRExtendedCable, and QRExtendedLocation.
```
# models.py
# Import NetBox and Django modules
# Abstract class which extended objects extend from
class QRObject(models.Model):

    photo = models.ImageField(upload_to='image-attachments/')
    url = models.URLField(default='', max_length=200)

    class Meta:
        abstract = True
```
Each of these models extend this QRObject class which defines photo fields, which holds the url to an objects photo, and an url field, which holds the html value to display the resized QR Code image in the table.

```
class QRExtendedDevice(QRObject):
    device = models.ForeignKey(
        to="dcim.Device", 
        on_delete=models.CASCADE, 
        null=True
    )

    def get_absolute_url(self):
        '''

    def get_status_class(self):
        '''

class QRExtendedRack(QRObject):
    rack = models.ForeignKey(
        to="dcim.Rack", 
        on_delete=models.CASCADE, 
        null=True
    )

    def get_absolute_url(self):
        '''

    def get_status_class(self):
        '''

class QRExtendedCable(QRObject):
    cable = models.ForeignKey(
        to="dcim.Cable", on_delete=models.CASCADE, null=True
    )

    def get_absolute_url(self):
        '''

    def get_status_class(self):
        '''

class QRExtendedLocation(QRObject):
    location = models.ForeignKey(
        to="dcim.Location", on_delete=models.CASCADE, null=True
    )

    def get_absolute_url(self):
        '''

    def get_status_class(self):
        '''
```
Each of the QRExtended models hold a reference to their corresponding base NetBox model object and define get_absolute_url() and get_status_class() function. The model only holds the object because any of its meta data can be accessed through that reference.

## Tables, Forms, and Filters
These 3 aspects heavily rely on the Django modules which NetBox heavily uses, instead of NetBox itself. 

### Tables
Tables represent the data which is displayed on the page. Fields are set up to look within the respective device, rack, cable, and location object.
Documentation: https://django-tables2.readthedocs.io/en/latest/

### Forms
Forms represent the search form that is used to filter for certain objects. This is accessed via the "Filters" tab on the plugin devices, racks, cables, and locations pages. Forms add parameters to the GET requests which Filtersets parse and utilize. The name of the fields in the form defines the key value for the url arguments.
Documentation: https://docs.djangoproject.com/en/4.1/topics/forms/

### Filtersets
Filtersets represent how to filter for objects using certain fields. This works internally by parsing and utilizing parameters in the GET requests, which can be seen in the url. The filtersets also define what fields to look in the given model to filter on.
Filtersets: https://www.django-rest-framework.org/api-guide/filtering/


### Adding New Models
Netbox Plugin Development Guide Documentation: https://docs.netbox.dev/en/stable/plugins/development/

When adding new models to the plugin, copying the structure of the already created models will usually suffice. Below is a list of directories to add new files to and files to modify.
```
- netbox_qrcode
    - templates/netbox_qrcode/{model_name}.html
    - __init__.py
    - admin.py
    - forms.py
    - models.py
    - navigation.py
    - tables.py
    - template_content.py
    - urls.py
    - views.py
```

### Making Migrations
After making the necessary modifications to the above files, ensure that the /etc/netbox/configuration.py file has `DEVELOPER = True". This can be set by modifying the netbox config map and restarting the netbox container.

Warning, whenever the netbox Deploy Helm process is run, the netbox configmap will reset.

Then, run the following commands within the container's shell: 
```
SECRET_KEY="dummy" /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py makemigrations
SECRET_KEY="dummy" /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate
```
If this is successful, copy the contents of the file(s) generated by makemigrations. They should be located in the following directory: `/opt/netbox/venv/lib/python3.10/site-packages/netbox_qrcode/migrations/`. The latest migration will have the highest number followed by brief description of the migration. This is necessary to keep the migrations in sync between different containers.

Create, add, and commit the whole file within the [netbox_qrcode/migrations/](netbox_qrcode/migrations/) directory.


## Contributing
Developing tools for this project based on [ntc-netbox-plugin-onboarding](https://github.com/networktocode/ntc-netbox-plugin-onboarding) repo.

Issues and pull requests are welcomed.

## Screenshots

Device QR code with text label
![Device QR Code](docs/img/qrcode.png)

Rack QR code
![Rack QR Code](docs/img/qrcode_rack.png)

Cable QR code
![Cable QR Code](docs/img/qrcode_cable.png)
