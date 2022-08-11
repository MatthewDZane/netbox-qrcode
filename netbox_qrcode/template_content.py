from packaging import version

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from extras.plugins import PluginTemplateExtension

from .utilities import get_img_b64, get_qr, get_qr_text, get_concat

class QRCode(PluginTemplateExtension):

    def x_page(self):
        config = self.context['config']
        obj = self.context['object']
        request = self.context['request']
        url = request.build_absolute_uri(obj.get_absolute_url())

        # Handle qr text if enabled
        if config.get('with_text'):
            base_url = request.build_absolute_uri('/') + 'media/image-attachments/'
            with_text_url = '{}{}.png'.format(base_url, obj._meta.object_name + str(obj.pk))
            img = with_text_url
            
        else:
            base_url = request.build_absolute_uri('/') + 'media/image-attachments/'
            no_text_url = '{}noText{}.png'.format(base_url, obj._meta.object_name + str(obj.pk))
            img = no_text_url
        try:
            if version.parse(settings.VERSION).major >= 3:
                return self.render(
                    'netbox_qrcode/qrcode3.html', extra_context={'image': img}
                )
            else:
                return self.render(
                    'netbox_qrcode/qrcode.html', extra_context={'image': img}
                )
        except ObjectDoesNotExist:
            return ''


class DeviceQRCode(QRCode):
    model = 'dcim.device'

    def right_page(self):
        return self.x_page()


class RackQRCode(QRCode):
    model = 'dcim.rack'

    def right_page(self):
        return self.x_page()


class CableQRCode(QRCode):
    model = 'dcim.cable'

    def left_page(self):
        return self.x_page()


class LocationQRCode(QRCode):
    model = 'dcim.location'

    def right_page(self):
        return self.x_page()


template_extensions = [DeviceQRCode, RackQRCode, CableQRCode, LocationQRCode]
