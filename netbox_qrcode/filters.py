import django_filters
from django.db import models

from dcim.models import Region, Site, Location, Rack, DeviceType, DeviceRole, RackRole
from dcim.choices import LinkStatusChoices, CableTypeChoices, DeviceStatusChoices, RackStatusChoices

from utilities.filters import (
    ContentTypeFilter, MultiValueNumberFilter, TreeNodeMultipleChoiceFilter,
)
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable, QRExtendedLocation

class BaseFiltersSet(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )


# Recieves QuerySet in Views.py and filters based on form values, returns the resulting filtered queryset back to views.py
class SearchDeviceFilterSet(BaseFiltersSet):
    status = django_filters.MultipleChoiceFilter(
        field_name='device__status',
        choices=DeviceStatusChoices,
        null_value=None
    )
    region = django_filters.ModelMultipleChoiceFilter(
        field_name='device__site__region',
        queryset=Region.objects.all(),
        label='Region (ID)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='device__site',
        queryset=Site.objects.all(),
        label='Site (ID)',
    )
    location = TreeNodeMultipleChoiceFilter(
        queryset=Location.objects.all(),
        field_name='device__location',
        lookup_expr='in',
        label='Location (ID)',
    )
    rack = django_filters.ModelMultipleChoiceFilter(
        field_name='device__rack',
        queryset=Rack.objects.all(),
        label='Rack (ID)',
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='device__device_role__slug',
        queryset=DeviceRole.objects.all(),
        to_field_name='slug',
        label='Role (slug)',
    )
    device_type = django_filters.ModelMultipleChoiceFilter(
        field_name='device__device_type_id',
        queryset=DeviceType.objects.all(),
        label='Device type (ID)',
    )
    class Meta:
        model = QRExtendedDevice
        fields = [
            'id', 
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(device__name__icontains=value) |
            models.Q(device_id__icontains=value.strip()) |
            models.Q(device__location__name__icontains=value.strip()) |
            models.Q(device__site__name__icontains=value.strip()) |
            models.Q(device__rack__name__icontains=value)
        ).distinct()

class SearchRackFilterSet(BaseFiltersSet):
    status = django_filters.MultipleChoiceFilter(
        field_name='rack__status',
        choices=RackStatusChoices,
        null_value=None
    )
    location = TreeNodeMultipleChoiceFilter(
        queryset=Location.objects.all(),
        field_name='rack__location',
        lookup_expr='in',
        label='Location (ID)',
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='rack__site',
        queryset=Site.objects.all(),
        label='Site (ID)',
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='rack__role_id',
        queryset=RackRole.objects.all(),
        label='Role (ID)',
    )

    class Meta:
        model = QRExtendedRack
        fields = [
            'id', 

        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(rack__name__icontains=value) |
            models.Q(rack_id__icontains=value.strip()) |
            models.Q(rack__location__name__icontains=value.strip()) |
            models.Q(rack__site__name__icontains=value.strip())
        ).distinct()

class SearchCableFilterSet(BaseFiltersSet):
    termination_a_type = ContentTypeFilter(
        field_name='cable__termination_a_type'
    )
    termination_a_id = MultiValueNumberFilter(
        field_name='cable__termination_a_id'
    )
    termination_b_type = ContentTypeFilter(
        field_name='cable__termination_b_type'
    )
    termination_b_id = MultiValueNumberFilter(
        field_name='cable__termination_b_id'
    )
    type = django_filters.MultipleChoiceFilter(
        choices=CableTypeChoices,
        field_name='cable__type'
    )
    status = django_filters.MultipleChoiceFilter(
        choices=LinkStatusChoices,
        field_name='cable__status'
    )
    device = MultiValueNumberFilter(
        method='filter_device',
        field_name='cable__device_id'
    )
    rack = MultiValueNumberFilter(
        method='filter_device',
        field_name='cable__device__rack_id'
    )
    site = MultiValueNumberFilter(
        method='filter_device',
        field_name='cable__device__site_id'
    )
    
    class Meta:
        model = QRExtendedCable
        fields = [
            'id',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(cable__id__icontains=value.strip()) |
            models.Q(cable__termination_a_type__name__icontains=value.strip()) |
            models.Q(cable__termination_a__name__icontains=value.strip()) |
            models.Q(cable__termination_a_type__name__icontains=value.strip()) |
            models.Q(cable__termination_a__name__icontains=value.strip()) 
        ).distinct()

    def filter_device(self, queryset, name, value):
        queryset = queryset.filter(
            models.Q(**{'cable___termination_a_{}__in'.format(name[7:]): value}) |
            models.Q(**{'cable___termination_b_{}__in'.format(name[7:]): value})
        )
        return queryset


class SearchLocationFilterSet(BaseFiltersSet):
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='location__site',
        queryset=Site.objects.all(),
        label='Site (ID)',
    )
    
    class Meta:
        model = QRExtendedLocation
        fields = [
            'id', 
            'location__description'
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(location__name__icontains=value.strip()) |
            models.Q(location__id__icontains=value.strip()) |
            models.Q(location__termination_a__name__icontains=value.strip()) |
            models.Q(location__site__name__icontains=value.strip()) 
        ).distinct()
