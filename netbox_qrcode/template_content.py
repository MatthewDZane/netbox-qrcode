
from django.core.exceptions import ObjectDoesNotExist
from extras.plugins import PluginTemplateExtension

from .utilities import get_img_b64, get_qr, get_qr_text, get_concat


class QRCode(PluginTemplateExtension):

    def x_page(self):
        config = self.context['config']
        obj = self.context['object']
        request = self.context['request']
        url = request.build_absolute_uri(obj.get_absolute_url())
        # get object settings
        obj_cfg = config.get(self.model.replace('dcim.', ''))
        if obj_cfg is None:
            return ''
        # and ovverride default
        config.update(obj_cfg)

        qr_args = {}
        for k, v in config.items():
            if k.startswith('qr_'):
                qr_args[k.replace('qr_', '')] = v

        qr_img = get_qr(url, **qr_args)
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
            text_img = get_qr_text(qr_img.size, text, config.get('font'))
            qr_with_text = get_concat(qr_img, text_img)
            img = get_img_b64(qr_with_text)
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
