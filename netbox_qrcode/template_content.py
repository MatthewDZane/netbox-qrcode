from django.core.exceptions import ObjectDoesNotExist
from extras.plugins import PluginTemplateExtension

from .utilities import get_img_b64, get_qr, get_qr_text, get_concat
import base64

class QRCode(PluginTemplateExtension):

    def x_page(self):
        config = self.context['config']
        obj = self.context['object']
        request = self.context['request']
        url = request.build_absolute_uri(obj.get_absolute_url())
        # Get object config settings
        obj_cfg = config.get(self.model.replace('dcim.', ''))
        if obj_cfg is None:
            return ''
        # and override default config
        config.update(obj_cfg)

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
                                text.append('{}'.format(getattr(obj, text_field).get(cfn)))
                        except AttributeError:
                            pass
                    else:
                        text.append('{}'.format(getattr(obj, text_field)))
            custom_text = config.get('custom_text')
            if custom_text:
                text.append(custom_text)
            text = '\n'.join(text)

            # Create qr text with image size and text
            text_img = get_qr_text(qr_img.size, text, 'ArialMT')

            # Combine qr image and qr text 
            qr_with_text = get_concat(qr_img, text_img)

            # Convert png to base 64 image
            img = get_img_b64(qr_with_text)
            
            # Save image with text to container with object's first field name
            text_fields = config.get('text_fields', [])
            file_path = '/opt/netbox/netbox/media/image-attachments/{}.png'.format(getattr(obj, text_fields[0], 'default'))
            qr_with_text.save(file_path)

            # Save image without text to container
            file_path = '/opt/netbox/netbox/media/image-attachments/noText{}.png'.format(getattr(obj, text_fields[0], 'default'))
            resize_width_height = (90,90)
            qr_img = qr_img.resize(resize_width_height)
            qr_img.save(file_path)

            # Resize final image for thumbnails and save
            resize_width_height = (150,75)
            qr_with_text = qr_with_text.resize(resize_width_height)
            file_path = '/opt/netbox/netbox/media/image-attachments/resized{}.png'.format(getattr(obj, text_fields[0], 'default'))
            qr_with_text.save(file_path)

        else:
            img = get_img_b64(qr_img)
        try:
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


template_extensions = [DeviceQRCode, RackQRCode, CableQRCode]
