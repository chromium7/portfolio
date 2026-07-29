from django.contrib import admin

from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0
    fields = ("image", "caption", "position")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "role", "is_visible", "updated_at")
    list_display_links = ("title",)
    list_editable = ("position", "is_visible")
    list_filter = ("is_visible",)
    search_fields = ("title", "role", "description", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "role", "description", "project_url")}),
        ("Tech Stack", {"fields": ("tech_stack",)}),
        ("Display", {"fields": ("position", "is_visible")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "position", "uploaded_at")
    list_filter = ("project", "uploaded_at")
    search_fields = ("caption", "project__title")
