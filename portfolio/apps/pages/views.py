from typing import Any

from django.db.models import QuerySet
from django.views.generic import DetailView, ListView, TemplateView

from portfolio.apps.events.models import Event, EventCategory
from portfolio.apps.projects.models import Project


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = (
            Project.objects.filter(is_visible=True)
            .prefetch_related("images")
            .order_by("position", "-created_at")
        )
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ProjectsView(TemplateView):
    template_name = "pages/projects.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = (
            Project.objects.filter(is_visible=True)
            .prefetch_related("images")
            .order_by("position", "-created_at")
        )
        return context


class ToolsView(TemplateView):
    template_name = "pages/tools.html"


class CreditsView(TemplateView):
    template_name = "pages/credits.html"


class EventsView(ListView):
    model = Event
    template_name = "pages/events.html"
    context_object_name = "events"
    ordering = ["-date"]
    paginate_by = 16

    def get_queryset(self) -> QuerySet[Event]:
        queryset = super().get_queryset().select_related("category").prefetch_related("photos")
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = EventCategory.objects.filter(events__isnull=False).distinct()
        context["selected_category"] = self.request.GET.get("category", "")
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "pages/event_detail.html"
    context_object_name = "event"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self) -> QuerySet[Event]:
        return super().get_queryset().select_related("category").prefetch_related("photos")
