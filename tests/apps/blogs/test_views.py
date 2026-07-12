from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from portfolio.apps.blogs.models import BlogPost

User = get_user_model()


class BlogListViewTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user(email="author@example.com", password="strong-pass-123")

    def test_list_only_shows_published_posts(self) -> None:
        published = BlogPost.objects.create(
            title="Published Post",
            content="Body",
            author=self.author,
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        BlogPost.objects.create(
            title="Draft Post",
            content="Body",
            author=self.author,
            status=BlogPost.Status.DRAFT,
        )

        response = self.client.get(reverse("blogs:list"))

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["posts"], [published])
        self.assertContains(response, "Published Post")
        self.assertNotContains(response, "Draft Post")


class BlogDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user(email="author@example.com", password="strong-pass-123")

    def test_published_post_is_visible(self) -> None:
        post = BlogPost.objects.create(
            title="Published Post",
            content="# Heading\n\nBody text",
            author=self.author,
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now(),
        )

        response = self.client.get(reverse("blogs:detail", kwargs={"slug": post.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published Post")
        self.assertContains(response, "<h1>Heading</h1>", html=True)

    def test_draft_post_returns_404(self) -> None:
        post = BlogPost.objects.create(
            title="Draft Post",
            content="Body",
            author=self.author,
            status=BlogPost.Status.DRAFT,
        )

        response = self.client.get(reverse("blogs:detail", kwargs={"slug": post.slug}))

        self.assertEqual(response.status_code, 404)
