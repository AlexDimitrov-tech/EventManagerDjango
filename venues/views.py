from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Venue
from .forms import VenueForm, VenueEditForm

def venue_list(request):
    venues = Venue.objects.all().order_by('name')
    return render(request, 'venues/list.html', {'venues': venues})

def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    events = venue.event_set.all()
    return render(request, 'venues/detail.html', {'venue': venue, 'events': events})

def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue created successfully.')
            return redirect('venue_list')
    else:
        form = VenueForm()
    return render(request, 'venues/form.html', {'form': form, 'title': 'Create Venue'})

def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == 'POST':
        form = VenueEditForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue updated successfully.')
            return redirect('venue_detail', pk=venue.pk)
    else:
        form = VenueEditForm(instance=venue)
    return render(request, 'venues/form.html', {'form': form, 'title': 'Edit Venue', 'venue': venue})

def venue_delete(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == 'POST':
        venue.delete()
        messages.success(request, 'Venue deleted successfully.')
        return redirect('venue_list')
    return render(request, 'venues/delete.html', {'venue': venue})

