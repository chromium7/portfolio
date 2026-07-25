from typing import Any

from django.db.models import QuerySet
from django.views.generic import DetailView, ListView, TemplateView

from portfolio.apps.events.models import Event


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ProjectsView(TemplateView):
    template_name = "pages/projects.html"


class ToolsView(TemplateView):
    template_name = "pages/tools.html"


class CreditsView(TemplateView):
    template_name = "pages/credits.html"


class EventsView(ListView):
    model = Event
    template_name = "pages/events.html"
    context_object_name = "events"
    ordering = ["-date"]
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Event]:
        return super().get_queryset().select_related("category").prefetch_related("photos")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories = Event.objects.values_list("category__name", flat=True).distinct()
        context["categories"] = sorted(categories)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "pages/event_detail.html"
    context_object_name = "event"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self) -> QuerySet[Event]:
        return super().get_queryset().select_related("category").prefetch_related("photos")
