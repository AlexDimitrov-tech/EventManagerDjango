from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Event
from venues.models import Venue
from categories.models import Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'categories', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter event description'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.Select(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }
        labels = {
            'title': 'Event Title',
            'description': 'Description',
            'date': 'Date',
            'time': 'Time',
            'venue': 'Venue',
            'categories': 'Categories',
            'price': 'Price',
        }
        help_texts = {
            'price': 'Enter price in currency units',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['venue'].queryset = Venue.objects.all().order_by('name')
        self.fields['categories'].queryset = Category.objects.all().order_by('name')

    def clean_date(self):
        event_date = self.cleaned_data.get('date')
        if event_date and event_date < date.today():
            raise ValidationError('Event date cannot be in the past.')
        return event_date

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Price cannot be negative.')
        return price

class EventEditForm(EventForm):
    created_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True, 'disabled': True}),
        label='Created At'
    )

    class Meta(EventForm.Meta):
        fields = ['title', 'description', 'date', 'time', 'venue', 'categories', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['created_at'].initial = self.instance.created_at

