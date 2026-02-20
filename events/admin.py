from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'venue']
    list_filter = ['date', 'venue']
    search_fields = ['title', 'description']

