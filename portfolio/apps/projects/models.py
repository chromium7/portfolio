from typing import Any

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from portfolio.core.utils import FilenameGenerator


class Project(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True, blank=True)
    role = models.CharField(_("role"), max_length=200, help_text=_("e.g. Fullstack Engineer, Lead Engineer"))
    description = models.TextField(_("description"))
    project_url = models.URLField(_("project URL"), blank=True, help_text=_("External link to the project"))
    tech_stack = ArrayField(
        models.CharField(max_length=100),
        verbose_name=_("tech stack"),
        blank=True,
        default=list,
        help_text=_("List of technologies used"),
    )
    image = models.ImageField(
        _("image"),
        upload_to=FilenameGenerator("projects"),
        blank=True,
        null=True,
        help_text=_("Project screenshot or thumbnail"),
    )
    position = models.PositiveIntegerField(_("position"), default=0, db_index=True)
    is_visible = models.BooleanField(_("visible"), default=True, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ("position", "-created_at")

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
