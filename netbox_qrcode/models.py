# Extends netbox models with Custom models
from django.db import models
from django.urls import reverse

from dcim.models import Device, Site, Region, Rack, Cable, DeviceRole, DeviceType, RackGroup, RackRole, Manufacturer
from dcim.choices import DeviceStatusChoices, RackStatusChoices, CableStatusChoices, RackTypeChoices
from ipam.choices import *

# Abstract class which extended devices extend from
class QRObject(models.Model):

    photo = models.ImageField(upload_to='image-attachments/')
    url = models.URLField(default='', max_length=200)

    class Meta:
        abstract = True

# Devices Wrapper
class QRExtendedDevice(QRObject):
    device = models.ForeignKey(to="dcim.Device", on_delete=models.CASCADE, null=True)

    name = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=50,
        choices=DeviceStatusChoices,
        default=DeviceStatusChoices.STATUS_ACTIVE
    )

    device_type = models.ForeignKey(
        to='dcim.DeviceType',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    device_role = models.ForeignKey(
        to='dcim.DeviceRole',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    rack = models.ForeignKey(
        to='dcim.Rack',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    # Set link for id column in QRDeviceTable to be the return url formatted with device's pk
    def get_absolute_url(self):
        return 'https://netbox.nrp-nautilus.io/dcim/devices/{}/'.format(self.device.pk)
    def get_status_class(self):
        return DeviceStatusChoices.CSS_CLASSES.get(self.status)

# Racks Wrapper
class QRExtendedRack(QRObject):
    rack = models.ForeignKey(to="dcim.Rack", on_delete=models.CASCADE, null=True)
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    facility_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Facility ID',
        help_text='Locally-assigned identifier'
    )

    status = models.CharField(
        max_length=50,
        choices=RackStatusChoices,
        default=RackStatusChoices.STATUS_ACTIVE
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    group = models.ForeignKey(
        to='dcim.RackGroup',
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True,
        null=True,
        help_text='Assigned group'
    )
    role = models.ForeignKey(
        to='dcim.RackRole',
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
        help_text='Functional role'
    )

    type = models.CharField(
        choices=RackTypeChoices,
        max_length=50,
        blank=True,
        verbose_name='Type'
    )

    def get_absolute_url(self):
        return 'https://netbox.nrp-nautilus.io/dcim/racks/{}/'.format(self.rack.pk)
    def get_status_class(self):
        return RackStatusChoices.CSS_CLASSES.get(self.status)

# Cables Wrapper
class QRExtendedCable(QRObject):
    cable = models.ForeignKey(to="dcim.Cable", on_delete=models.CASCADE, null=True)
    
    _termination_a_device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    _termination_b_device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True
    )
    def get_absolute_url(self):
        return 'https://netbox.nrp-nautilus.io/dcim/cables/{}/'.format(self.cable.pk)
    def get_status_class(self):
        return CableStatusChoices.CSS_CLASSES.get(self.status)