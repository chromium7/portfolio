from typing import Any

from django.db import models
from django.utils.text import slugify


def event_photo_upload_path(instance: "EventPhoto", filename: str) -> str:
    return f"events/{instance.event.id}/{filename}"


class EventCategory(models.Model):
    class Group(models.TextChoices):
        RUNNING = "running", "Running"
        CYCLING = "cycling", "Cycling"
        TRIATHLON = "triathlon", "Triathlon"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    group = models.CharField(max_length=20, choices=Group.choices, default=Group.OTHER)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Event categories"
        ordering = ["group", "name"]

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    class ResultType(models.TextChoices):
        TIME = "time", "Time-based"
        SCORE = "score", "Score-based"
        PLACEMENT = "placement", "Placement only"

    name = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory, on_delete=models.PROTECT, related_name="events")
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    result_type = models.CharField(max_length=20, choices=ResultType.choices, default=ResultType.TIME)

    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    finish_time = models.DurationField(null=True, blank=True)

    overall_position = models.PositiveIntegerField(null=True, blank=True)
    category_position = models.PositiveIntegerField(null=True, blank=True)
    score = models.CharField(max_length=100, blank=True)

    bib_number = models.CharField(max_length=20, blank=True)
    strava_url = models.URLField(blank=True)
    official_result_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["-date"]), models.Index(fields=["category"])]

    @property
    def pace_per_km(self) -> "datetime.timedelta | None":
        if self.finish_time and self.distance_km and self.distance_km > 0:
            return self.finish_time / float(self.distance_km)
        return None

    def __str__(self) -> str:
        return f"{self.name} ({self.date.year})"


class EventPhoto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to=event_photo_upload_path)
    caption = models.CharField(max_length=200, blank=True)
    is_cover = models.BooleanField(default=False, help_text="Use as the main thumbnail for this event")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_cover", "uploaded_at"]

    def __str__(self) -> str:
        return f"Photo for {self.event.name}"
