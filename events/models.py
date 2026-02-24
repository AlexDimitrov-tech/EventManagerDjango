from django.db import models
from django.urls import reverse
from datetime import date


STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('cancelled', 'Cancelled'),
]

STATUS_COLORS = {
    'published': 'success',
    'cancelled': 'danger',
    'draft': 'secondary',
}


class EventManager(models.Manager):

    def upcoming(self):
        # only show published future events on the homepage
        return self.get_queryset().filter(date__gte=date.today(), status='published')


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    venue = models.ForeignKey(
        'venues.Venue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    categories = models.ManyToManyField(
        'categories.Category',
        blank=True,
        related_name='events'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    def is_free(self):
        return self.price == 0

    def is_past(self):
        return self.date < date.today()

    def get_price_display_str(self):
        if self.price == 0:
            return 'Free'
        return f'${self.price}'

    def get_status_color(self):
        return STATUS_COLORS.get(self.status, 'secondary')

    def clean(self):
        from django.core.exceptions import ValidationError
        # don't let someone publish an event that's already passed
        if self.date and self.date < date.today() and self.status == 'published':
            raise ValidationError('Cannot publish events that are in the past.')
