from django.views.generic import TemplateView


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
