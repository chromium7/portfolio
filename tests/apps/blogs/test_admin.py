from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from portfolio.apps.blogs.models import BlogPost

User = get_user_model()


class BlogPostAdminTests(TestCase):
    def setUp(self) -> None:
        self.staff_user = User.objects.create_user(
            email="staff@example.com",
            password="strong-pass-123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.staff_user)

    def test_changelist_loads(self) -> None:
        response = self.client.get(reverse("admin:blogs_blogpost_changelist"))

        self.assertEqual(response.status_code, 200)

    def test_add_page_renders_markdown_editor_widget(self) -> None:
        response = self.client.get(reverse("admin:blogs_blogpost_add"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "markdownx-editor")

    def test_can_create_post_via_admin(self) -> None:
        response = self.client.post(
            reverse("admin:blogs_blogpost_add"),
            data={
                "title": "Admin Created Post",
                "slug": "",
                "author": self.staff_user.pk,
                "status": BlogPost.Status.DRAFT,
                "excerpt": "",
                "content": "# Hello",
            },
        )

        self.assertEqual(response.status_code, 302)
        post = BlogPost.objects.get(title="Admin Created Post")
        self.assertEqual(post.slug, "admin-created-post")
