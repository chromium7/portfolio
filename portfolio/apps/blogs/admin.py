from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
    date_hierarchy = "published_at"
    list_display = ("title", "author", "status", "published_at", "updated_at")
    list_filter = ("status", "author")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("author",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "status", "published_at")}),
        ("Content", {"fields": ("excerpt", "featured_image", "content")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
