# venues/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.VenueListView.as_view(), name='venue_list'),
    path('new/', views.venue_create, name='venue_create'),
    path('<int:pk>/', views.venue_detail, name='venue_detail'),
    path('<int:pk>/edit/', views.venue_edit, name='venue_edit'),
    path('<int:pk>/delete/', views.venue_delete, name='venue_delete'),
]
