from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Location(models.Model):
    title = models.CharField("location title", max_length=50)
    url = models.CharField("information link", max_length=100)
    lat = models.FloatField("latitude")
    lon = models.FloatField("longitude")
    # TODO: add created_at, updated_at


class Event(models.Model):
    title = models.CharField("event title", max_length=50)
    description = models.CharField("event description", max_length=250)
    date = models.DateTimeField("event date")
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    # TODO: add participants, photos and videos, created_at, updated_at
