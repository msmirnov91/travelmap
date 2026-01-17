from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
import os


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


class MediaFile(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    description = models.TextField(blank=True, verbose_name="description")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at"
    )

    def __str__(self):
        return f"{self.title}"

    def get_file_type(self):
        return self._meta.verbose_name

    def get_file_url(self):
        raise NotImplementedError("Implement this method in subclasses")

    class Meta:
        abstract = True
        ordering = ['title']


class Image(MediaFile):
    file = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        verbose_name="Изображение",
        help_text="Загрузите изображение (макс. 10MB)",
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        )]
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Превью",
        editable=False
    )
    width = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Ширина",
        editable=False
    )
    height = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Высота",
        editable=False
    )

    def get_file_url(self):
        return self.file.url if self.file else None

    def save(self, *args, **kwargs):
        if self.file:
            super().save(*args, **kwargs)

            img = PilImage.open(self.file.path)
            self.update_size(img)

            if not self.thumbnail:
                self.update_thumbnail(img)

        super().save(*args, **kwargs)

    def update_size(self, img):
        self.width, self.height = img.size

    def update_thumbnail(self, img):
        img.thumbnail((300, 300))

        thumb_io = BytesIO()
        if img.mode in ('RGBA', 'LA'):
            img = img.convert('RGB')

        img.save(thumb_io, format='JPEG', quality=85)

        thumb_name = f"thumb_{os.path.basename(self.file.name).split('.')[0]}.jpg"
        self.thumbnail.save(
            thumb_name,
            ContentFile(thumb_io.getvalue()),
            save=False
        )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Video(MediaFile):
    file = models.FileField(
        upload_to='videos/%Y/%m/%d/',
        verbose_name="Видео файл",
        help_text="Загрузите видео (макс. 100MB)",
        validators=[FileExtensionValidator(
            allowed_extensions=['mp4', 'avi', 'mov', 'mkv', 'webm', 'wmv', 'flv']
        )]
    )
    thumbnail = models.ImageField(
        upload_to='video_thumbs/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Превью видео"
    )
    duration = models.DurationField(
        blank=True,
        null=True,
        verbose_name="Продолжительность"
    )
    resolution = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Разрешение"
    )
    file_size = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Размер файла (байт)",
        editable=False
    )

    def get_file_url(self):
        return self.file.url if self.file else None

    def get_file_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class MediaGallery(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    images = models.ManyToManyField(
        Image,
        blank=True,
        verbose_name="Изображения"
    )
    videos = models.ManyToManyField(
        Video,
        blank=True,
        verbose_name="Видео"
    )

    def get_all_media(self):
        all_media = []
        all_media.extend(self.images.all())
        all_media.extend(self.videos.all())
        return sorted(all_media, key=lambda x: x.title, reverse=True)

