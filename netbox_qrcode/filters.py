import django_filters
from django.db import models

from dcim.models import Device, Site, Region, Rack, DeviceRole, DeviceType, Manufacturer, RackGroup, RackRole
from dcim.choices import DeviceStatusChoices, RackStatusChoices, RackTypeChoices, RackWidthChoices, CableStatusChoices, CableTypeChoices

from utilities.choices import ColorChoices
from utilities.filters import TreeNodeMultipleChoiceFilter, MultiValueNumberFilter, MultiValueCharFilter

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
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    region = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='site__region',
        lookup_expr='in',
        to_field_name='slug',
        label='Region (slug)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='site__slug',
        queryset=Site.objects.all(),
        to_field_name='slug',
        label='Site (slug)',
    )
    group = TreeNodeMultipleChoiceFilter(
        queryset=RackGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        to_field_name='slug',
        label='Rack group (slug)',
    )
    status = django_filters.MultipleChoiceFilter(
        choices=RackStatusChoices,
        null_value=None
    )
    type = django_filters.MultipleChoiceFilter(
        choices=RackTypeChoices
    )
    width = django_filters.MultipleChoiceFilter(
        choices=RackWidthChoices
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='role__slug',
        queryset=RackRole.objects.all(),
        to_field_name='slug',
        label='Role (slug)',
    )
    serial = django_filters.CharFilter(
        lookup_expr='iexact'
    )

    class Meta:
        model = QRExtendedRack
        fields = ['id', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(name__icontains=value)
        )



class SearchCableFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    type = django_filters.MultipleChoiceFilter(
        choices=CableTypeChoices
    )
    status = django_filters.MultipleChoiceFilter(
        choices=CableStatusChoices
    )
    color = django_filters.MultipleChoiceFilter(
        choices=ColorChoices
    )
    device = MultiValueCharFilter(
        method='filter_device',
        field_name='device__name'
    )
    rack = MultiValueNumberFilter(
        method='filter_device',
        field_name='device__rack__name'
    )
    site = MultiValueNumberFilter(
        method='filter_device',
        field_name='device__site__slug'
    )
    tenant = MultiValueNumberFilter(
        method='filter_device',
        field_name='device__tenant__slug'
    )

    class Meta:
        model = QRExtendedCable
        fields = ['id', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(label__icontains=value)




