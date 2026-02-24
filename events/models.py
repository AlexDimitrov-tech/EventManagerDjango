from django.db import models
from django.urls import reverse
from datetime import date


STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('cancelled', 'Cancelled'),
]


class EventManager(models.Manager):

    def upcoming(self):
        today = date.today()
        qs = self.get_queryset()
        qs = qs.filter(date__gte=today)
        qs = qs.filter(status='published')
        return qs

    def published_only(self):
        qs = self.get_queryset()
        result = qs.filter(status='published')
        return result


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
        if self.price == 0:
            return True
        else:
            return False

    def is_past(self):
        today = date.today()
        if self.date < today:
            return True
        else:
            return False

    def get_price_display_str(self):
        if self.price == 0:
            price_str = 'Free'
        else:
            price_str = '$' + str(self.price)
        return price_str

    def get_status_color(self):
        if self.status == 'published':
            color = 'success'
        elif self.status == 'cancelled':
            color = 'danger'
        else:
            color = 'secondary'
        return color

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date is not None:
            today = date.today()
            if self.date < today:
                if self.status == 'published':
                    raise ValidationError('Cannot publish events that are in the past.')
