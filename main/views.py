from django.views.generic import DetailView, CreateView, UpdateView
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy

from .models import Profile, Location, Event
from .forms import LocationForm, EventForm


def index(request):
    limit = 10
    locations = Location.objects.all()[:limit]
    events = Event.objects.all()[:limit]

    template = loader.get_template("main/index.html")
    context = {
        "locations": locations,
        "events": events,
    }
    return HttpResponse(template.render(context, request))


def profile(request, profile_id):
    profile = Profile.objects.filter(id=profile_id).first()
    template = loader.get_template("main/profile.html")
    context = {"profile": profile}
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template("main/about.html")
    context = {}
    return HttpResponse(template.render(context, request))


class LocationDetailView(DetailView):
    model = Location
    template_name = "main/location_detail.html"
    context_object_name = "location"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Место: {self.object.title}"
        return context


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = "main/location_form.html"
    success_message = "Место успешно создано!"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Создание нового места"
        context["submit_text"] = "Создать место"
        return context

    def get_success_url(self):
        return reverse_lazy('location', kwargs={'pk': self.object.pk})


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "main/location_form.html"
    success_message = "Место успешно обновлено!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование: {self.object.title}"
        context["submit_text"] = "Сохранить изменения"
        return context

    def get_queryset(self):
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('location', kwargs={'pk': self.object.pk})


class EventDetailView(DetailView):
    model = Event
    template_name = "main/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Поездка: {self.object.title}"
        return context


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "main/event_form.html"
    success_message = "Поездка успешно создана!"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Создание новой поездки"
        context["submit_text"] = "Создать поездку"
        return context

    def get_success_url(self):
        return reverse_lazy('event', kwargs={'pk': self.object.pk})


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "main/event_form.html"
    success_message = "Поездка успешно обновлена!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование: {self.object.title}"
        context["submit_text"] = "Сохранить изменения"
        return context

    def get_queryset(self):
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('event', kwargs={'pk': self.object.pk})
