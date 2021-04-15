from django import forms
from dcim.models import Device, Site, Region, Rack, Cable, DeviceRole, DeviceType, RackGroup, RackRole, Manufacturer
from dcim.choices import DeviceStatusChoices, RackStatusChoices, RackTypeChoices, RackWidthChoices, CableStatusChoices, CableTypeChoices

from utilities.forms import DynamicModelMultipleChoiceField, StaticSelect2Multiple
from .models import QRExtendedDevice, QRExtendedRack, QRExtendedCable


class SearchFilterFormDevice(forms.Form):

    model = QRExtendedDevice

    q = forms.CharField(
        required=False,
        label='Search'
    )

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='slug',
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=DeviceStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        to_field_name='id',
        required=False,
        label='Device',
        null_option='None',
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label='Rack',
        null_option='None',
    )

    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'region': '$region'
        }
    )
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        required=False,
        label='Manufacturer'
    )

    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label='Model',
        display_field='model',
        query_params={
            'manufacturer': '$manufacturer'
        }
    )

class SearchFilterFormRack(forms.Form):

    model = QRExtendedRack
    
    q = forms.CharField(
        required=False,
        label='Search'
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='slug',
        required=False
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'region': '$region'
        }
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=RackGroup.objects.all(),
        required=False,
        label='Rack group',
        null_option='None',
        query_params={
            'site': '$site'
        }
    )
    status = forms.MultipleChoiceField(
        choices=RackStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
    type = forms.MultipleChoiceField(
        choices=RackTypeChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )

    class Meta:
        model = Rack
        fields = [
            'region', 'site', 'group', 'name', 'facility_id', 'tenant_group', 'tenant', 'status', 'role', 'serial',
            'asset_tag', 'type', 'width', 'u_height', 'desc_units', 'outer_width', 'outer_depth', 'outer_unit',
            'comments', 'tags',
        ]

class SearchFilterFormCable(forms.Form):

    model = QRExtendedCable
    
    q = forms.CharField(
        required=False,
        label='Search'
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='slug',
        required=False
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label='Rack',
        null_option='None',
    )

    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'region': '$region'
        }
    )