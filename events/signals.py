from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date


from .models import Event


@receiver(pre_save, sender=Event)
def auto_cancel_past_published_events(sender, instance, **kwargs):
    event_date = instance.date
    event_status = instance.status
    today = date.today()

    is_in_past = event_date < today
    is_published = event_status == 'published'
    is_published_and_past = is_in_past and is_published

    if is_published_and_past:
        instance.status = 'cancelled'
