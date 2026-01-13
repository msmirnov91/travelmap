from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("main/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def event(request, event_id):
    template = loader.get_template("main/event.html")
    context = {"event_id": event_id}
    return HttpResponse(template.render(context, request))
