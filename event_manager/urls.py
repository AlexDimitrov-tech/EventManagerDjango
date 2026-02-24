# event_manager/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('venues/', include('venues.urls')),
    path('categories/', include('categories.urls')),
]

# custom 404 page - need this for the exam requirement
handler404 = 'events.views.handler_404'
