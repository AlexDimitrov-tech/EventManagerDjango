from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            raw_name = self.name
            category_name_slug = slugify(raw_name)
            self.slug = category_name_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_list')

    def get_event_count(self):
        published_events = self.events.filter(status='published')
        total = published_events.count()
        return total

    def has_any_events(self):
        total = self.events.count()
        if total > 0:
            return True
        else:
            return False
