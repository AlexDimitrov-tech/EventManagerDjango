from django.db import models
from django.urls import reverse
from datetime import date


class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.city})'

    def get_absolute_url(self):
        return reverse('venue_detail', kwargs={'pk': self.pk})

    def get_upcoming_events(self):
        today = date.today()
        upcoming = []
        for event in self.events.all():
            if event.date >= today:
                upcoming.append(event)
        return upcoming

    def is_available_on(self, check_date):
        return not self.events.filter(date=check_date).exists()

    def get_size_label(self):
        cap = self.capacity
        if cap < 50:
            return 'Intimate'
        elif cap < 200:
            return 'Small'
        elif cap < 1000:
            return 'Medium'
        return 'Large'
