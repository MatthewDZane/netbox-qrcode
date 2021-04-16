import django_filters
from django.db import models

from dcim.models import Device, Site, Region, Rack, DeviceRole, DeviceType, Manufacturer
from dcim.choices import DeviceStatusChoices

from utilities.filters import TreeNodeMultipleChoiceFilter
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable


# Recieves QuerySet in Views.py and filters based on form values, returns the resulting filtered queryset back to views.py
class SearchDeviceFilterSet(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    status = django_filters.MultipleChoiceFilter(
        choices=DeviceStatusChoices,
        null_value=None
    )

    region = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='site__region',
        lookup_expr='in',
        to_field_name='slug',
        label='Region (slug)',
    )

    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset= QRExtendedDevice.objects.all(),
        to_field_name='id',
        field_name='id',
        label='Device (ID)',
    )

    rack_id = django_filters.ModelMultipleChoiceFilter(
        field_name='rack',
        queryset=Rack.objects.all(),
        label='Rack (ID)',
    )

    site = django_filters.ModelMultipleChoiceFilter(
        field_name='site__slug',
        queryset=Site.objects.all(),
        to_field_name='slug',
        label='Site name (slug)',
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__manufacturer__slug',
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        label='Manufacturer (slug)',
    )
    model = django_filters.ModelMultipleChoiceFilter(
        field_name='device_type__slug',
        queryset=DeviceType.objects.all(),
        to_field_name='slug',
        label='Device model (slug)',
    )

    class Meta:
        model = QRExtendedDevice
        fields = ['id', ]
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(name__icontains=value)
        )

class SearchRackFilterSet(django_filters.FilterSet):

    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label='Site (ID)',
    )
    region_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='site__region',
        label='Region (ID)',
    )

    class Meta:
        model = QRExtendedRack
        fields = ['id', ]



class SearchCableFilterSet(django_filters.FilterSet):

    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=QRExtendedCable.objects.all(),
        to_field_name='id',
        field_name='id',
        label='Device (ID)',
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        label='Site (ID)',
    )
    region_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='site__region',
        label='Region (ID)',
    )

    class Meta:
        model = QRExtendedCable
        fields = ['id', ]


