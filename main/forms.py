from django.contrib.gis import forms as gis_forms
from django import forms
from .models import Location, Event


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["title", "url", "coordinates"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите название"
            }),
            "url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ссылку"
            }),
            "coordinates": gis_forms.OSMWidget(attrs={
                "default_lat": 55.7558,
                "default_lon": 37.6173,
                "default_zoom": 13,
            }),
        }
        labels = {
            "title": "Название места",
            "url": "Ссылка с информацией о месте",
            "coordinates": "Координаты",
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date", "location"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите название"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Введите описание"
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "location": forms.Select(attrs={
                "class": "form-select",
                "placeholder": "Выберите место"
            }),
        }
        labels = {
            "title": "Название поездки",
            "description": "Описание поездки",
            "date": "Дата",
            "location": "Место",
        }
