from django import forms
from datetime import date

from .models import Event, STATUS_CHOICES
from venues.models import Venue
from categories.models import Category


class EventForm(forms.ModelForm):
    # keeping title and date explicit so we can set proper error messages
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event title'}),
        error_messages={
            'required': 'Title is required.',
            'max_length': 'Title is too long, keep it under 200 chars.',
        }
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={'required': 'Date is required.', 'invalid': 'Not a valid date.'}
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'categories', 'price', 'status', 'max_attendees']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the event...'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank for unlimited'}),
        }
        help_texts = {
            'price': 'Set to 0 for free events.',
            'max_attendees': 'Optional — leave blank if unlimited.',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters.')
        return title

    def clean_date(self):
        event_date = self.cleaned_data.get('date')
        if event_date and event_date < date.today():
            raise forms.ValidationError('The event date cannot be in the past.')
        return event_date

    def clean(self):
        cleaned = super().clean()
        venue = cleaned.get('venue')
        event_date = cleaned.get('date')

        # venue conflict check lives here rather than the model because
        # we need both venue and date from the form at the same time
        if venue and event_date:
            conflicts = Event.objects.filter(venue=venue, date=event_date)
            if conflicts.exists():
                raise forms.ValidationError(
                    f'That venue already has {conflicts.count()} event(s) on this date.'
                )

        return cleaned


class EventEditForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Title is required.'}
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={'required': 'Date is required.', 'invalid': 'Invalid date.'}
    )
    created_at = forms.CharField(
        required=False,
        label='Created at',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'disabled': 'disabled',
        }),
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'categories', 'price', 'status', 'max_attendees']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.CheckboxSelectMultiple(),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.created_at:
            self.fields['created_at'].initial = self.instance.created_at.strftime('%Y-%m-%d %H:%M')

    def clean_title(self):
        t = self.cleaned_data.get('title', '').strip()
        if len(t) < 3:
            raise forms.ValidationError('Title is too short.')
        return t

    def clean(self):
        cleaned = super().clean()
        venue = cleaned.get('venue')
        event_date = cleaned.get('date')

        if venue and event_date:
            existing = Event.objects.filter(venue=venue, date=event_date).exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(
                    f'Venue is already booked on this date ({existing.count()} event(s)).'
                )

        return cleaned
