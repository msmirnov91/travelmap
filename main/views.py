from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Profile, Location, Event


def index(request):
    limit = 10
    locations = Location.objects.all()[:limit]
    events = Event.objects.all()[:limit]

    template = loader.get_template("main/index.html")
    context = {
        'locations': locations,
        'events': events,
    }
    return HttpResponse(template.render(context, request))


def profile(request, profile_id):
    profile = Profile.objects.filter(id=profile_id).first()
    template = loader.get_template("main/profile.html")
    context = {"profile": profile}
    return HttpResponse(template.render(context, request))


def location(request, location_id):
    location = Location.objects.filter(id=location_id).first()
    template = loader.get_template("main/location.html")
    context = {"location": location}
    return HttpResponse(template.render(context, request))


def event(request, event_id):
    event = Event.objects.filter(id=event_id).first()
    template = loader.get_template("main/event.html")
    context = {"event": event}
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template("main/about.html")
    context = {}
    return HttpResponse(template.render(context, request))
