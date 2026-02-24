from django import forms
from datetime import date

from .models import Event, STATUS_CHOICES
from venues.models import Venue
from categories.models import Category


class EventForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event title'}),
        help_text='Enter a descriptive title for your event.',
        error_messages={
            'required': 'Title is required.',
            'max_length': 'Title is too long, keep it under 200 chars.',
        }
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the event...'}),
        help_text='Optional but recommended.',
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='Pick the event date.',
        error_messages={
            'required': 'Date is required.',
            'invalid': 'Not a valid date.',
        }
    )
    time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        help_text='Optional — leave blank if time is TBD.',
    )
    venue = forms.ModelChoiceField(
        queryset=Venue.objects.all().order_by('name'),
        required=False,
        empty_label='-- No venue selected --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Choose a venue if you have one.',
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text='Pick one or more categories.',
    )
    price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        initial=0.00,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        help_text='Set to 0 for free events.',
        error_messages={
            'required': 'Price is required.',
            'invalid': 'Enter a valid price.',
        }
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        initial='draft',
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={'required': 'Status is required.'}
    )
    max_attendees = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank for unlimited'}),
        help_text='Maximum number of attendees. Leave blank if unlimited.',
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'categories', 'price', 'status', 'max_attendees']

    def clean_title(self):
        title_value = self.cleaned_data.get('title')
        if title_value is not None:
            stripped = title_value.strip()
            if len(stripped) < 3:
                raise forms.ValidationError('Title must be at least 3 characters.')
            return stripped
        return title_value

    def clean_date(self):
        event_date = self.cleaned_data.get('date')
        if event_date is not None:
            today = date.today()
            if event_date < today:
                raise forms.ValidationError('The event date cannot be in the past.')
        return event_date

    def clean(self):
        cleaned = super().clean()
        chosen_venue = cleaned.get('venue')
        chosen_date = cleaned.get('date')

        if chosen_venue is not None and chosen_date is not None:
            conflicts = Event.objects.filter(venue=chosen_venue, date=chosen_date)
            if conflicts.exists():
                conflict_count = conflicts.count()
                raise forms.ValidationError(
                    'That venue already has ' + str(conflict_count) + ' event(s) on this date.'
                )

        return cleaned


class EventEditForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Event title.',
        error_messages={
            'required': 'Title is required.',
            'max_length': 'Too long.',
        }
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={
            'required': 'Date is required.',
            'invalid': 'Invalid date.',
        }
    )
    time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
    )
    venue = forms.ModelChoiceField(
        queryset=Venue.objects.all().order_by('name'),
        required=False,
        empty_label='-- No venue --',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        error_messages={
            'required': 'Price is required.',
            'invalid': 'Enter a valid price.',
        }
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    max_attendees = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    created_at = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'disabled': 'disabled'}),
        label='Created at',
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'categories', 'price', 'status', 'max_attendees']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            created = self.instance.created_at
            if created is not None:
                self.fields['created_at'].initial = created.strftime('%Y-%m-%d %H:%M')

    def clean_title(self):
        t = self.cleaned_data.get('title')
        if t:
            t = t.strip()
            if len(t) < 3:
                raise forms.ValidationError('Title is too short.')
        return t

    def clean(self):
        cleaned = super().clean()
        chosen_venue = cleaned.get('venue')
        chosen_date = cleaned.get('date')

        if chosen_venue is not None and chosen_date is not None:
            existing = Event.objects.filter(venue=chosen_venue, date=chosen_date)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            count = existing.count()
            if count > 0:
                raise forms.ValidationError(
                    'Venue is already booked on this date (' + str(count) + ' event(s)).'
                )

        return cleaned
