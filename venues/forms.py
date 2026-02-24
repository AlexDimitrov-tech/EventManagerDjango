from django import forms
from .models import Venue


class VenueForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue name'}),
        help_text='Full name of the venue.',
        error_messages={'required': 'Please enter the venue name.'}
    )
    address = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address'}),
        help_text='Street address.',
        error_messages={'required': 'Address is required.'}
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        help_text='City where the venue is located.',
        error_messages={'required': 'City is required.'}
    )
    capacity = forms.IntegerField(
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        help_text='Max number of people. Enter 0 if unknown.',
        error_messages={
            'required': 'Capacity is required.',
            'invalid': 'Enter a number.',
            'min_value': 'Cannot be negative.',
        }
    )
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555-000-1234'}),
        help_text='Contact phone number (optional).',
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@venue.com'}),
        help_text='Contact email (optional).',
        error_messages={'invalid': 'Enter a valid email address.'}
    )

    class Meta:
        model = Venue
        fields = ['name', 'address', 'city', 'capacity', 'phone', 'email']

    def clean_phone(self):
        phone_value = self.cleaned_data.get('phone')
        if phone_value:
            phone_stripped = phone_value.strip()
            allowed_chars = set('0123456789 +-.()')
            for ch in phone_stripped:
                if ch not in allowed_chars:
                    raise forms.ValidationError('Phone can only contain numbers and + - . ( ) characters.')
            return phone_stripped
        return phone_value

    def clean_capacity(self):
        cap = self.cleaned_data.get('capacity')
        if cap is not None:
            if cap > 500000:
                raise forms.ValidationError('That capacity seems unrealistically high.')
        return cap


class VenueEditForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Venue name.',
        error_messages={'required': 'Name is required.'}
    )
    address = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Address is required.'}
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'City is required.'}
    )
    capacity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Capacity is required.',
            'invalid': 'Enter a number.',
            'min_value': 'Cannot be negative.',
        }
    )
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Enter a valid email.'}
    )
    created_at = forms.CharField(
        required=False,
        label='Created at',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'disabled': 'disabled'}),
    )

    class Meta:
        model = Venue
        fields = ['name', 'address', 'city', 'capacity', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            c = self.instance.created_at
            if c is not None:
                self.fields['created_at'].initial = c.strftime('%Y-%m-%d %H:%M')

    def clean_phone(self):
        phone_val = self.cleaned_data.get('phone')
        if phone_val:
            stripped = phone_val.strip()
            ok_chars = set('0123456789 +-.()')
            for char in stripped:
                if char not in ok_chars:
                    raise forms.ValidationError('Phone number has invalid characters.')
            return stripped
        return phone_val

    def clean_capacity(self):
        capacity_val = self.cleaned_data.get('capacity')
        if capacity_val is not None:
            if capacity_val > 500000:
                raise forms.ValidationError('That is way too high for a venue capacity.')
        return capacity_val
