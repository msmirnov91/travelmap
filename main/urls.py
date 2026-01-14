from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:profile_id>/", views.profile, name="profile"),
    path("location/<int:location_id>/", views.location, name="location"),
    path("event/<int:event_id>/", views.event, name="event"),
    path("about/", views.about, name="about"),
]
