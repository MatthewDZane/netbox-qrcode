from django import forms
from dcim.models import Device, Site, Region, Rack, Cable, DeviceRole, DeviceType, RackGroup, RackRole, Manufacturer
from dcim.choices import DeviceStatusChoices

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