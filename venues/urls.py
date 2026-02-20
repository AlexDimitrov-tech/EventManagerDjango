from django.urls import path
from . import views

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('<int:pk>/', views.venue_detail, name='venue_detail'),
    path('create/', views.venue_create, name='venue_create'),
    path('<int:pk>/edit/', views.venue_edit, name='venue_edit'),
    path('<int:pk>/delete/', views.venue_delete, name='venue_delete'),
]

