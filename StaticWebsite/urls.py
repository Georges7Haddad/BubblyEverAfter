from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("legal", views.legal),
    path("contact", views.contact),
    path("about", views.about),
    path("burningman", views.burningman),
    path("events", views.display_events),
    path("create_event", views.create_event),
    path("display_events", views.display_events),
]
