from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("events/<int:event_id>/", views.event, name="event"),
    path("about/", views.about, name="about"),
]
