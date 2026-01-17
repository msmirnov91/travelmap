from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Location(models.Model):
    title = models.CharField("location title", max_length=50, unique=True)
    url = models.URLField(
        "information link",
        max_length=500,
        help_text="Введите полный URL, включая https://",
        blank=True,
        null=True,
    )
    coordinates = gis_models.PointField(
        geography=True,  # Для сферических расчетов (WGS84)
        srid=4326,  # Система координат WGS84
        verbose_name='Координаты',
        unique=True,
        null=True,
    )
    updated = models.DateTimeField("updated at", auto_now=True)
    updated_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='updated_locations',
        default=1,
    )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("location", kwargs={"pk": self.pk})

    class Meta:
        indexes = [
            models.Index(fields=['-updated'])
        ]


class Event(models.Model):
    title = models.CharField("event title", max_length=50, unique=True)
    description = models.CharField("event description", max_length=250)
    date = models.DateField("event date")
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="events",
    )
    updated = models.DateTimeField("updated at", auto_now=True)
    updated_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='updated_events',
        default=1,
    )
    participants = models.ManyToManyField(
        Profile,
        related_name='visited_events'
    )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("event", kwargs={"pk": self.pk})

    class Meta:
        indexes = [
            models.Index(fields=['-updated'])
        ]
