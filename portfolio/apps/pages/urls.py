from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("tools/", views.ToolsView.as_view(), name="tools"),
    path("credits/", views.CreditsView.as_view(), name="credits"),
]
