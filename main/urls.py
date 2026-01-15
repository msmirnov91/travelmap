from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:profile_id>/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path(
        "location/<int:location_id>/",
        views.LocationDetailView.as_view(),
        name="location"
    ),
    path(
        "location/create/",
        views.LocationCreateView.as_view(),
        name="location-create"
    ),
    path(
        "location/<int:location_id>/update/",
        views.LocationUpdateView.as_view(),
        name="location-update"
    ),
    path(
        "event/<int:event_id>/",
        views.EventDetailView.as_view(),
        name="event"
    ),
    path(
        "event/create/",
        views.EventCreateView.as_view(),
        name="event-create"
    ),
    path(
        "event/<int:event_id>/update/",
        views.EventUpdateView.as_view(),
        name="event-update"
    ),
]
