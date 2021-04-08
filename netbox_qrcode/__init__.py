from extras.plugins import PluginConfig
from .version import __version__


class QRCodeConfig(PluginConfig):
    name = 'netbox_qrcode_ui'
    verbose_name = 'QR Code View'   # Subtitle to dropdown
    description = 'Generate QR codes for the objects'
    version = __version__
    author = 'Jason Lin'
    author_email = 'jasonlin1198@gmail.com'
    required_settings = []
    default_settings = {
        'with_text': True,
        'text_fields': ['name', 'serial'],
        'font': 'ArialMT',
        'custom_text': None,
        'qr_version': 1,
        'qr_error_correction': 0,
        'qr_box_size': 6,
        'qr_border': 4,
        'device': {
            'text_fields': ['name', 'serial']
        },
        'rack': {
            'text_fields': ['name']
        },
        'cable': {
            'text_fields': [
                '_termination_a_device',
                'termination_a',
                '_termination_b_device',
                'termination_b',
                ]
        }
    }

config = QRCodeConfig # noqa E305