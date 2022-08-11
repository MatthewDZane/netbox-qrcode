# Extends netbox models with Custom models
from django.db import models
from django.urls import reverse

from dcim.choices import DeviceStatusChoices, RackStatusChoices, LinkStatusChoices
from ipam.choices import *


# Abstract class which extended objects extend from
class QRObject(models.Model):

    photo = models.ImageField(upload_to='image-attachments/')
    url = models.URLField(default='', max_length=200)

    class Meta:
        abstract = True


class QRExtendedDevice(QRObject):
    """
    Devices Wrapper
    """
    device = models.ForeignKey(
        to="dcim.Device", 
        on_delete=models.CASCADE, 
        null=True
    )

    def get_absolute_url(self):
        """
        # Set link for id column in QRDeviceTable to be the return url formatted with device's pk
        """
        return reverse('dcim:device', args=[self.device.pk])

    def get_status_class(self):
        return DeviceStatusChoices.CSS_CLASSES.get(self.status)


class QRExtendedRack(QRObject):
    """
    Racks Wrapper
    """
    rack = models.ForeignKey(
        to="dcim.Rack", 
        on_delete=models.CASCADE, 
        null=True
    )

    def get_absolute_url(self):
        return reverse('dcim:rack', args=[self.rack.pk])

    def get_status_class(self):
        return RackStatusChoices.CSS_CLASSES.get(self.status)


class QRExtendedCable(QRObject):
    """
    Cables Wrapper
    """
    cable = models.ForeignKey(
        to="dcim.Cable", on_delete=models.CASCADE, null=True
    )

    def get_absolute_url(self):
        return reverse('dcim:cable', args=[self.cable.pk])

    def get_status_class(self):
        return LinkStatusChoices.CSS_CLASSES.get(self.status)


class QRExtendedLocation(QRObject):
    """
    Locations Wrapper
    """
    location = models.ForeignKey(
        to="dcim.Location", on_delete=models.CASCADE, null=True
    )

    def get_absolute_url(self):
        return reverse('dcim:location', args=[self.location.pk])

    def get_status_class(self):
        return LinkStatusChoices.CSS_CLASSES.get(self.status)
