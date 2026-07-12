from django.db.models import QuerySet
from django.views.generic import DetailView, ListView

from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = "blogs/list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[BlogPost]:
        return BlogPost.objects.published()


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blogs/detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self) -> QuerySet[BlogPost]:
        return BlogPost.objects.published()
