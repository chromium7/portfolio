from django.contrib import admin

from .models import Event, EventCategory, EventPhoto


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 0
    fields = ("image", "caption", "is_cover")


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "typical_distance_km")
    list_filter = ("group",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("name", "category", "date", "location", "result_type")
    list_filter = ("result_type", "category", "date")
    search_fields = ("name", "location", "notes")
    readonly_fields = ("created_at", "updated_at")
    inlines = [EventPhotoInline]
    fieldsets = (
        (None, {"fields": ("name", "category", "date", "location", "result_type")}),
        ("Result", {"fields": ("distance_km", "finish_time", "pace_per_km", "score", "overall_position", "category_position")}),
        ("Details", {"fields": ("bib_number", "official_result_url", "notes")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ("event", "caption", "is_cover", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("caption", "event__name")
