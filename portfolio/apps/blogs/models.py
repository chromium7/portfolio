from typing import Any

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField

from portfolio.core.utils import FilenameGenerator


class BlogPostQuerySet(models.QuerySet):
    def published(self) -> "BlogPostQuerySet":
        return self.filter(status=BlogPost.Status.PUBLISHED, published_at__lte=timezone.now())


class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")

    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )
    excerpt = models.TextField(_("excerpt"), blank=True, help_text=_("Short summary shown in the post list."))
    content = MarkdownxField(_("content"))
    featured_image = models.ImageField(
        _("featured image"),
        upload_to=FilenameGenerator("blogs/featured"),
        blank=True,
        null=True,
    )
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(_("published at"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = BlogPostQuerySet.as_manager()

    class Meta:
        verbose_name = _("blog post")
        verbose_name_plural = _("blog posts")
        ordering = ("-published_at", "-created_at")
        indexes = (models.Index(fields=("status", "published_at")),)

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blogs:detail", kwargs={"slug": self.slug})
