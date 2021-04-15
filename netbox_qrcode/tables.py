import django_tables2 as tables
from utilities.tables import BaseTable, ChoiceFieldColumn, ColoredLabelColumn
from dcim.models import Device, Rack, Site, Cable
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable
from django.utils.safestring import mark_safe

class ToggleColumn(tables.CheckBoxColumn):
    """
    Extend CheckBoxColumn to add a "toggle all" checkbox in the column header.
    """
    def __init__(self, *args, **kwargs):
        default = kwargs.pop('default', '')
        visible = kwargs.pop('visible', True)
        if 'attrs' not in kwargs:
            kwargs['attrs'] = {
                'td': {
                    'class': 'min-width'
                }
            }
        super().__init__(*args, default=default, visible=visible, **kwargs)

    @property
    def header(self):
        return mark_safe('<input type="checkbox" class="toggle" title="Toggle all" />')



# Device Table
class QRDeviceTables(BaseTable):
    """Table for displaying Device objects."""

    # Set up hyperlinks to column items
    pk = ToggleColumn()
    device = tables.LinkColumn()
    status = ChoiceFieldColumn()
    device_role = ColoredLabelColumn()
    device_type = tables.LinkColumn()
    rack = tables.LinkColumn()
    site = tables.LinkColumn()
    id = tables.LinkColumn()
    qrcode = tables.TemplateColumn('<img src="{{record.url}}"> ')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedDevice
        fields = (
            "pk",
            "device",
            "status",
            "device_role",
            "device_type",
            "rack",
            "site",
            "id",
            "photo",
            "qrcode",
        )

# Rack Table
class QRRackTables(BaseTable):
    """Table for displaying Rack objects."""

    # Set up hyperlinks to column items
    pk = ToggleColumn()
    rack = tables.LinkColumn()
    status = ChoiceFieldColumn()
    site = tables.LinkColumn()
    group = tables.LinkColumn()
    role = ColoredLabelColumn()
    id = tables.LinkColumn()
    qrcode = tables.TemplateColumn('<img src="{{record.url}}"> ')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedRack
        fields = (
            "pk",
            "rack",
            "status",
            "site",
            "group",
            "role",
            "id",
            "photo",
            "qrcode",
        )

# Cable Table
class QRCableTables(BaseTable):
    """Table for displaying Cable objects."""

    # Set up hyperlinks to column items
    pk = ToggleColumn()
    cable = tables.LinkColumn()
    id = tables.LinkColumn()
    qrcode = tables.TemplateColumn('<img src="{{record.url}}"> ')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedCable
        fields = (
            "pk",
            "cable",
            "id",
            "photo",
            "qrcode",
        )
