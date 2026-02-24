# events/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/new/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
]
