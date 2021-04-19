from django import forms
from dcim.models import Device, Site, Region, Rack, Cable, DeviceRole, RackGroup, RackRole, Manufacturer
from dcim.choices import DeviceStatusChoices, RackStatusChoices, RackTypeChoices, CableStatusChoices, CableTypeChoices

from utilities.forms import DynamicModelMultipleChoiceField, StaticSelect2Multiple, DynamicModelChoiceField


class BaseFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='slug',
        required=False,
        initial_params={
            'sites': '$site'
        }
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'region': '$region'
        }
    )


class SearchFilterFormDevice(BaseFilterForm):

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
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='slug',
        required=False,
        label='Manufacturer'
    )


class SearchFilterFormRack(BaseFilterForm):

    status = forms.MultipleChoiceField(
        choices=RackStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
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
    type = forms.MultipleChoiceField(
        choices=RackTypeChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
    role = DynamicModelChoiceField(
        queryset=RackRole.objects.all(),
        required=False
    )


class SearchFilterFormCable(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    status = forms.MultipleChoiceField(
        choices=CableStatusChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
    type = forms.MultipleChoiceField(
        choices=CableTypeChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
