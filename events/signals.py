from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date

from .models import Event


# using a signal here so this runs even on admin saves,
# not just through the form
@receiver(pre_save, sender=Event)
def auto_cancel_past_published_events(sender, instance, **kwargs):
    if instance.date < date.today() and instance.status == 'published':
        instance.status = 'cancelled'
