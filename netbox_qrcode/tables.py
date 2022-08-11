import django_tables2 as tables
from django_tables2.utils import Accessor

from netbox.tables import BaseTable, columns
from dcim.tables.template_code import CABLE_TERMINATION_PARENT

from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable, QRExtendedLocation


# Device Table
class QRDeviceTables(BaseTable):
    """Table for displaying Device objects."""
    pk = columns.ToggleColumn(visible=True)
    device = tables.LinkColumn()
    id = tables.LinkColumn()
    device__status = columns.ChoiceFieldColumn()
    device__site__region = tables.LinkColumn()
    device__site = tables.LinkColumn()
    device__location = tables.LinkColumn()
    device__rack = tables.LinkColumn()
    device__device_role = columns.ColoredLabelColumn()
    device__device_type = tables.LinkColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedDevice
        fields = (
            "pk",
            "device",
            "id",
            "device__status",
            "device__site__region",
            "device__site",
            "device__location",
            "device__rack",
            "device__device_role",
            "device__device_type",
            "photo",
            "url",
        )

# Rack Table
class QRRackTables(BaseTable):
    """Table for displaying Rack objects."""
    pk = columns.ToggleColumn(visible=True)
    rack = tables.LinkColumn()
    id = tables.LinkColumn()
    rack__status = columns.ChoiceFieldColumn()
    rack__site = tables.LinkColumn()
    rack__location = tables.LinkColumn()
    rack__role = columns.ColoredLabelColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedRack
        fields = (
            "pk",
            "rack",
            "id",
            "rack__status",
            "rack__location",
            "rack__site",
            "rack__role",
            "photo",
            "url",
        )

# Cable Table
class QRCableTables(BaseTable):
    """Table for displaying Cable objects."""

    # Set up hyperlinks to column items
    pk = columns.ToggleColumn(visible=True)
    cable = tables.LinkColumn()
    id = tables.LinkColumn()
    termination_a_parent = tables.TemplateColumn(
        template_code=CABLE_TERMINATION_PARENT,
        accessor=Accessor('cable__termination_a'),
        orderable=False,
        verbose_name='Side A'
    )
    rack_a = tables.Column(
        accessor=Accessor('cable__termination_a__device__rack'),
        orderable=False,
        linkify=True,
        verbose_name='Rack A'
    )
    termination_a = tables.Column(
        accessor=Accessor('cable__termination_a'),
        orderable=False,
        linkify=True,
        verbose_name='Termination A'
    )
    termination_b_parent = tables.TemplateColumn(
        template_code=CABLE_TERMINATION_PARENT,
        accessor=Accessor('cable__termination_b'),
        orderable=False,
        verbose_name='Side B'
    )
    rack_b = tables.Column(
        accessor=Accessor('cable__termination_b__device__rack'),
        orderable=False,
        linkify=True,
        verbose_name='Rack B'
    )
    termination_b = tables.Column(
        accessor=Accessor('cable__termination_b'),
        orderable=False,
        linkify=True,
        verbose_name='Termination B'
    )
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedCable
        fields = (
            "pk",
            "cable",
            "id",
            'cable__label', 
            'termination_a_parent', 
            'rack_a', 
            'termination_a', 
            'termination_b_parent', 
            'rack_b', 
            'termination_b',
            "cable__status",
            "photo",
            "url",
        )


# Location Table
class QRLocationTables(BaseTable):
    """Table for displaying Location objects."""
    pk = columns.ToggleColumn(visible=True)
    location = tables.LinkColumn()
    id = tables.LinkColumn()
    location__site = tables.LinkColumn()
    url = tables.TemplateColumn('<img src="{{record.url}}"> ', verbose_name = 'QR Code')

    # Netbox base table class, fields display column names/order
    class Meta(BaseTable.Meta):
        model = QRExtendedLocation
        fields = (
            "pk",
            "location",
            "id",
            "location__site",
            "photo",
            "url",
        )
