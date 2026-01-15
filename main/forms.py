from django import forms
from .models import Location, Event


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["title", "url", "lat", "lon"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите название"
            }),
            "url": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ссылку"
            }),
            "lat": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00"
            }),
            "lon": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "0.00"
            }),
        }
        labels = {
            "title": "Название места",
            "url": "Ссылка с информацией о месте",
            "lat": "Широта",
            "lon": "Долгота",
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date"]
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
            "date": forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }
        labels = {
            "title": "Название поездки",
            "description": "Описание поездки",
            "date": "Дата",
        }
