from django import forms
from dcim.models import Device, Site, Region, Rack, RackRole, Location
from dcim.choices import DeviceStatusChoices, RackStatusChoices, LinkStatusChoices

from utilities.forms import StaticSelect, DynamicModelMultipleChoiceField, StaticSelectMultiple, DynamicModelChoiceField
from .models import QRExtendedCable

class BaseFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search'
    )
    id = forms.IntegerField(
        required=False,
        label='ID'
    )


class SearchFilterFormDevice(BaseFilterForm):

    status = forms.MultipleChoiceField(
        choices=DeviceStatusChoices,
        required=False,
        widget=StaticSelectMultiple()
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
            'region': '$region',
            'location': '$location'
        }
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'sites': '$site'
        }
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label='Rack',
        null_option='None',
    )

class SearchFilterFormRack(BaseFilterForm):

    status = forms.MultipleChoiceField(
        choices=RackStatusChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'region': '$region',
            'location': '$location'
        }
    )
    location = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'sites': '$site'
        }
    )
    role = DynamicModelChoiceField(
        queryset=RackRole.objects.all(),
        to_field_name='slug',
        required=False,
        null_option='None',
    )


class SearchFilterFormCable(BaseFilterForm):
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        to_field_name='slug',
        required=False,
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
    )
    rack = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label='Rack',
        null_option='None',
    )
    type = forms.MultipleChoiceField(
        choices=LinkStatusChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    status = forms.MultipleChoiceField(
        choices=LinkStatusChoices,
        required=False,
        widget=StaticSelectMultiple()
    )

    class Meta:
        model = QRExtendedCable
        fields = [
            'type', 'status', 'label',
        ]
        widgets = {
            'status': StaticSelect,
            'type': StaticSelect,
        }


class SearchFilterFormLocation(BaseFilterForm):
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=False,
        query_params={
            'region': '$region',
            'location': '$location'
        }
    )
