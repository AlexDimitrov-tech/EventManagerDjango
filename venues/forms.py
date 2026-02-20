from django import forms
from .models import Venue

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue address'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
        }
        labels = {
            'name': 'Venue Name',
            'address': 'Address',
            'capacity': 'Capacity',
        }
        help_texts = {
            'capacity': 'Maximum number of attendees',
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity and capacity < 1:
            raise forms.ValidationError('Capacity must be at least 1.')
        return capacity

class VenueEditForm(VenueForm):
    created_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'disabled': True}),
        label='Created At'
    )

    class Meta(VenueForm.Meta):
        fields = ['name', 'address', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['created_at'].initial = self.instance.created_at

