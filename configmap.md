PLUGINS_CONFIG = {
    'netbox_qrcode': {
        'with_text': True,
        'text_fields': ['name', 'serial'],
        'font': 'ArialMT',
        'custom_text': 'Property of SomeCompany\ntel.8.800333554-CALL',
        'qr_version': 1,
        'qr_error_correction': 0,
        'qr_box_size': 4,
        'qr_border': 4,
        # per object options
        'cable': None,  # disable QR code for Cable object
        'rack': {
            'text_fields': [
                'site',
                'name',
                'facility_id',
                'tenant',
                'cf.cf_name'
            ]
        },
        'device': {
            'qr_box_size': 6,
            'custom_text': None,
        }
    }
}
