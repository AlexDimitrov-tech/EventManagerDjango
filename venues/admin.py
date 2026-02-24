from django.contrib import admin
from .models import Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity']
    search_fields = ['name', 'city']
