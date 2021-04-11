<pre>
PLUGINS = ['netbox_qrcode', 'nextbox_ui_plugin', 'netbox-bgp']
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        'with_text': True,
        'text_fields': ['name', 'asset_tag', 'serial', 'device_type'],
        'font': 'ComicSansMSBold',
        'custom_text': 'Pacific Research Platform (Nautilus)',
        'qr_version': 1,
        'qr_error_correction': 0,
        'qr_box_size': 2,
        'qr_border': 40,
        'cable': None,  # disable QR code for Cable object
        'rack': {
            'text_fields': ['site', 'name', 'facility_id', 'tenant']
        },
        'device': {
            'with_text': True,
            'text_fields': ['name', 'asset_tag', 'serial', 'device_type'],
            'font': 'ComicSansMSBold',
            'qr_version': 1,
            'qr_box_size': 2,
            'qr_border': 40,
        }
    }
}
