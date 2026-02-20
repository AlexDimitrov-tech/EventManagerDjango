from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import date
from .models import Event
from .forms import EventForm, EventEditForm
from venues.models import Venue
from categories.models import Category

def home(request):
    upcoming_events = Event.objects.filter(date__gte=date.today()).order_by('date', 'time')[:6]
    venues = Venue.objects.all()[:5]
    categories = Category.objects.all()[:5]
    return render(request, 'events/home.html', {
        'upcoming_events': upcoming_events,
        'venues': venues,
        'categories': categories,
    })

def event_list(request):
    events = Event.objects.all()
    
    search = request.GET.get('search', '')
    venue_filter = request.GET.get('venue', '')
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'date')
    
    if search:
        events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    if venue_filter:
        events = events.filter(venue_id=venue_filter)
    
    if category_filter:
        events = events.filter(categories__id=category_filter)
    
    if sort_by == 'title':
        events = events.order_by('title')
    elif sort_by == 'price':
        events = events.order_by('price')
    else:
        events = events.order_by('date', 'time')
    
    venues = Venue.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    
    return render(request, 'events/list.html', {
        'events': events,
        'venues': venues,
        'categories': categories,
        'search': search,
        'selected_venue': venue_filter,
        'selected_category': category_filter,
        'sort_by': sort_by,
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/form.html', {'form': form, 'title': 'Create Event'})

def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventEditForm(instance=event)
    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Event', 'event': event})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('event_list')
    return render(request, 'events/delete.html', {'event': event})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

