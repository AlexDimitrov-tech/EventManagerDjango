from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView

from .forms import VenueForm, VenueEditForm
from .models import Venue


class VenueListView(ListView):
    model = Venue
    template_name = 'venues/list.html'
    context_object_name = 'venues'

    def get_queryset(self):
        all_of_them = Venue.objects.all()
        ordered = all_of_them.order_by('name')
        return ordered

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_venues_list = list(Venue.objects.all().order_by('name'))
        context['total_count'] = len(all_venues_list)
        return context


def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    all_venue_events = venue.events.all()
    events_list = list(all_venue_events)

    upcoming_ones = []
    for ev in events_list:
        if not ev.is_past():
            upcoming_ones.append(ev)

    past_ones = []
    for ev in events_list:
        if ev.is_past():
            past_ones.append(ev)

    ctx = {
        'venue': venue,
        'upcoming_events': upcoming_ones,
        'past_events': past_ones,
    }
    return render(request, 'venues/detail.html', ctx)


def venue_create(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            v = form.save()
            venue_name = v.name
            messages.success(request, 'Venue "' + venue_name + '" added!')
            return redirect('venue_list')
        else:
            messages.error(request, 'Something went wrong, check the form.')
    else:
        form = VenueForm()

    return render(request, 'venues/form.html', {'form': form, 'page_title': 'Add Venue'})


def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == 'POST':
        form = VenueEditForm(request.POST, instance=venue)
        is_valid = form.is_valid()
        if is_valid:
            form.save()
            messages.success(request, f'Venue "{venue.name}" updated.')
            return redirect('venue_detail', pk=venue.pk)
        else:
            messages.error(request, 'Check the errors below.')
    else:
        form = VenueEditForm(instance=venue)

    ctx = {
        'form': form,
        'venue': venue,
        'page_title': 'Edit ' + venue.name,
    }
    return render(request, 'venues/edit_form.html', ctx)


def venue_delete(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == 'POST':
        name = venue.name
        venue.delete()
        messages.success(request, name + ' has been removed.')
        return redirect('venue_list')

    return render(request, 'venues/delete.html', {'venue': venue})
