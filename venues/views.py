from django.shortcuts import render, redirect, get_object_or_404
from .models import Venue
from .forms import VenueForm


def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'venues/list.html', {'venues': venues})


def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    return render(request, 'venues/detail.html', {
        'venue': venue,
        'events': venue.event_set.all(),
    })


def venue_create(request):
    # simpler way to handle form
    form = VenueForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect('venue_list')
    
    return render(request, 'venues/form.html', {
        'form': form, 
        'title': 'Create Venue'
    })


def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venue_detail', pk=pk)
    return render(request, 'venues/form.html', {'form': form, 'title': 'Edit Venue', 'venue': venue})


def venue_delete(request, pk):
    v = get_object_or_404(Venue, pk=pk)
    
    if request.method == 'POST':
        # confirm deletion
        v.delete()
        return redirect('venue_list')
    
    return render(request, 'venues/delete.html', {'venue': v})
