from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView

from categories.models import Category
from venues.models import Venue
from .forms import EventForm, EventEditForm
from .models import Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_obj = self.object
        cats = event_obj.categories.all()
        context['event_categories'] = cats
        return context


def home(request):
    upcoming_events = Event.objects.upcoming().select_related('venue')
    upcoming_list = list(upcoming_events)

    if len(upcoming_list) > 6:
        upcoming_list = upcoming_list[:6]

    venues_qs = Venue.objects.all().order_by('name')
    some_venues = list(venues_qs[:4])

    categories_qs = Category.objects.all().order_by('name')
    some_categories = list(categories_qs[:6])

    ctx = {
        'upcoming_events': upcoming_list,
        'some_venues': some_venues,
        'some_categories': some_categories,
    }
    return render(request, 'events/home.html', ctx)


def event_list(request):
    from django.db.models import Q

    all_events = Event.objects.all()
    all_events = all_events.select_related('venue')
    all_events = all_events.prefetch_related('categories')

    search_query = request.GET.get('search', '')
    search_query = search_query.strip()

    if len(search_query) > 0:
        q_filter = Q(title__icontains=search_query) | Q(description__icontains=search_query)
        all_events = all_events.filter(q_filter)

    selected_venue_id = request.GET.get('venue', '')
    if selected_venue_id != '':
        all_events = all_events.filter(venue__id=selected_venue_id)

    selected_category_id = request.GET.get('category', '')
    if selected_category_id != '':
        all_events = all_events.filter(categories__id=selected_category_id)
        all_events = all_events.distinct()

    sort_by = request.GET.get('sort', 'date')

    if sort_by == 'title':
        all_events = all_events.order_by('title')
    elif sort_by == 'price_low':
        all_events = all_events.order_by('price')
    elif sort_by == 'price_high':
        all_events = all_events.order_by('-price')
    else:
        all_events = all_events.order_by('date', 'time')

    venues_for_filter = Venue.objects.all().order_by('name')
    categories_for_filter = Category.objects.all().order_by('name')

    context = {
        'events': all_events,
        'all_venues': venues_for_filter,
        'all_categories': categories_for_filter,
        'search_query': search_query,
        'selected_venue_id': selected_venue_id,
        'selected_category_id': selected_category_id,
        'sort_by': sort_by,
    }
    return render(request, 'events/list.html', context)


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save()
            title = new_event.title
            messages.success(request, 'Event "' + title + '" was created successfully!')
            return redirect('event_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = EventForm()

    ctx = {
        'form': form,
        'page_title': 'Add New Event',
    }
    return render(request, 'events/form.html', ctx)


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event_pk = event.pk

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{event.title}" was updated.')
            return redirect('event_detail', pk=event_pk)
        messages.error(request, 'There are some errors, please check the form.')
    else:
        form = EventEditForm(instance=event)

    ctx = {
        'form': form,
        'event': event,
        'page_title': 'Edit: ' + event.title,
    }
    return render(request, 'events/edit_form.html', ctx)


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'"{title}" has been deleted.')
        return redirect('event_list')

    return render(request, 'events/delete.html', {'event': event})


def handler_404(request, exception):
    return render(request, '404.html', status=404)
