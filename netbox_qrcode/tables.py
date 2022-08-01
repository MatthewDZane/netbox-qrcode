import django_tables2 as tables
from netbox.tables import BaseTable, columns
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable, QRExtendedLocation

# Device Table
class QRDeviceTables(BaseTable):
    """Table for displaying Device objects."""

    # Set up hyperlinks to column items
    pk = columns.ToggleColumn(visible=True)
    device = tables.LinkColumn()
    status = columns.ChoiceFieldColumn()
    device_role = columns.ColoredLabelColumn()
    device_type = tables.LinkColumn()
    rack = tables.LinkColumn()
    site = tables.LinkColumn()
    id = tables.LinkColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

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
            "url",
        )

# Rack Table
class QRRackTables(BaseTable):
    """Table for displaying Rack objects."""

    # Set up hyperlinks to column items
    pk = columns.ToggleColumn(visible=True)
    rack = tables.LinkColumn()
    status = columns.ChoiceFieldColumn()
    site = tables.LinkColumn()
    role = columns.ColoredLabelColumn()
    id = tables.LinkColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedRack
        fields = (
            "pk",
            "rack",
            "site",
            "status",
            "role",
            "id",
            "photo",
            "url",
        )

# Cable Table
class QRCableTables(BaseTable):
    """Table for displaying Cable objects."""

    # Set up hyperlinks to column items
    pk = columns.ToggleColumn(visible=True)
    cable = tables.LinkColumn()
    # status = columns.ChoiceFieldColumn()
    id = tables.LinkColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedCable
        fields = (
            "pk",
            "cable",
            "id",
            "photo",
            "url",
        )


# Location Table
class QRLocationTables(BaseTable):
    """Table for displaying Location objects."""

    # Set up hyperlinks to column items
    pk = columns.ToggleColumn(visible=True)
    location = tables.LinkColumn()
    # status = columns.ChoiceFieldColumn()
    id = tables.LinkColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedLocation
        fields = (
            "pk",
            "location",
            "id",
            "photo",
            "url",
        )