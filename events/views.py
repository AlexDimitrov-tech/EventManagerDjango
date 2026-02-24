from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
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
        context['event_categories'] = self.object.categories.all()
        return context


def home(request):
    upcoming_events = Event.objects.upcoming().select_related('venue')[:6]
    some_venues = Venue.objects.order_by('name')[:4]
    some_categories = Category.objects.order_by('name')[:6]

    return render(request, 'events/home.html', {
        'upcoming_events': upcoming_events,
        'some_venues': some_venues,
        'some_categories': some_categories,
    })


def event_list(request):
    events = Event.objects.select_related('venue').prefetch_related('categories')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    selected_venue_id = request.GET.get('venue', '')
    if selected_venue_id:
        events = events.filter(venue__id=selected_venue_id)

    selected_category_id = request.GET.get('category', '')
    if selected_category_id:
        # distinct needed because the M2M join can produce duplicate rows
        events = events.filter(categories__id=selected_category_id).distinct()

    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'title':
        events = events.order_by('title')
    elif sort_by == 'price_low':
        events = events.order_by('price')
    elif sort_by == 'price_high':
        events = events.order_by('-price')
    else:
        events = events.order_by('date')

    return render(request, 'events/list.html', {
        'events': events,
        'all_venues': Venue.objects.order_by('name'),
        'all_categories': Category.objects.order_by('name'),
        'search_query': search_query,
        'selected_venue_id': selected_venue_id,
        'selected_category_id': selected_category_id,
        'sort_by': sort_by,
    })


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" was created successfully!')
            return redirect('event_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = EventForm()

    return render(request, 'events/form.html', {'form': form, 'page_title': 'Add New Event'})


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{event.title}" was updated.')
            return redirect('event_detail', pk=event.pk)
        messages.error(request, 'There are some errors, please check the form.')
    else:
        form = EventEditForm(instance=event)

    return render(request, 'events/edit_form.html', {
        'form': form,
        'event': event,
        'page_title': f'Edit: {event.title}',
    })


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
