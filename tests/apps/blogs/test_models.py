from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from portfolio.apps.blogs.models import BlogPost

User = get_user_model()


def _make_post(**overrides: object) -> BlogPost:
    author = (
        overrides.pop("author", None)
        or User.objects.get_or_create(email="author@example.com", defaults={"password": "strong-pass-123"})[0]
    )
    defaults = {
        "title": "My First Post",
        "content": "# Hello world",
        "author": author,
        "status": BlogPost.Status.DRAFT,
    }
    defaults.update(overrides)
    return BlogPost.objects.create(**defaults)


class BlogPostModelTests(TestCase):
    def test_str_returns_title(self) -> None:
        post = _make_post(title="Hello World")

        self.assertEqual(str(post), "Hello World")

    def test_save_generates_slug_from_title(self) -> None:
        post = _make_post(title="A Great Post Title!")

        self.assertEqual(post.slug, "a-great-post-title")

    def test_save_preserves_explicit_slug(self) -> None:
        post = _make_post(title="A Great Post Title!", slug="custom-slug")

        self.assertEqual(post.slug, "custom-slug")

    def test_slug_must_be_unique(self) -> None:
        author = User.objects.create_user(email="author@example.com", password="strong-pass-123")
        _make_post(title="Duplicate Title", author=author)

        with self.assertRaises(IntegrityError):
            _make_post(title="Duplicate Title", author=author)

    def test_get_absolute_url(self) -> None:
        post = _make_post(title="A Great Post Title!")

        self.assertEqual(post.get_absolute_url(), f"/blog/{post.slug}/")


class BlogPostQuerySetTests(TestCase):
    def test_published_excludes_drafts(self) -> None:
        _make_post(title="Draft Post", status=BlogPost.Status.DRAFT)
        published = _make_post(
            title="Published Post",
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now(),
        )

        self.assertCountEqual(BlogPost.objects.published(), [published])

    def test_published_excludes_future_scheduled_posts(self) -> None:
        _make_post(
            title="Scheduled Post",
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now() + timezone.timedelta(days=1),
        )

        self.assertFalse(BlogPost.objects.published().exists())
