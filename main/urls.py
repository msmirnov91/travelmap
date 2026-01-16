from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:profile_id>/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path(
        "location/<int:pk>/",
        views.LocationDetailView.as_view(),
        name="location"
    ),
    path(
        "location/create/",
        views.LocationCreateView.as_view(),
        name="location-create"
    ),
    path(
        "location/<int:pk>/update/",
        views.LocationUpdateView.as_view(),
        name="location-update"
    ),
    path(
        "event/<int:pk>/",
        views.EventDetailView.as_view(),
        name="event"
    ),
    path(
        "event/create/",
        views.EventCreateView.as_view(),
        name="event-create"
    ),
    path(
        "event/<int:pk>/update/",
        views.EventUpdateView.as_view(),
        name="event-update"
    ),
]
