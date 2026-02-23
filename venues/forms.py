from django import forms
from .models import Venue


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full address'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'capacity': 'Maximum number of attendees',
        }

    def clean_capacity(self):
        cap = self.cleaned_data.get('capacity')
        if cap is not None and cap < 1:
            raise forms.ValidationError('Has to be at least 1.')
        return cap
