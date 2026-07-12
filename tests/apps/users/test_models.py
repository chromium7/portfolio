from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self) -> None:
        user = User.objects.create_user(email="jane@example.com", password="strong-pass-123")

        self.assertEqual(user.email, "jane@example.com")
        self.assertTrue(user.check_password("strong-pass-123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_normalizes_email_domain(self) -> None:
        user = User.objects.create_user(email="jane@EXAMPLE.COM", password="strong-pass-123")

        self.assertEqual(user.email, "jane@example.com")

    def test_create_user_without_email_raises(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="strong-pass-123")

    def test_create_superuser(self) -> None:
        user = User.objects.create_superuser(email="admin@example.com", password="strong-pass-123")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_requires_is_staff_true(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="admin@example.com", password="strong-pass-123", is_staff=False)

    def test_create_superuser_requires_is_superuser_true(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="admin@example.com", password="strong-pass-123", is_superuser=False)


class UserModelTests(TestCase):
    def test_email_is_username_field(self) -> None:
        self.assertEqual(User.USERNAME_FIELD, "email")
        self.assertEqual(User.REQUIRED_FIELDS, [])

    def test_str_returns_email(self) -> None:
        user = User.objects.create_user(email="jane@example.com", password="strong-pass-123")

        self.assertEqual(str(user), "jane@example.com")

    def test_get_full_name_and_short_name(self) -> None:
        user = User.objects.create_user(
            email="jane@example.com",
            password="strong-pass-123",
            first_name="Jane",
            last_name="Doe",
        )

        self.assertEqual(user.get_full_name(), "Jane Doe")
        self.assertEqual(user.get_short_name(), "Jane")

    def test_email_must_be_unique(self) -> None:
        User.objects.create_user(email="jane@example.com", password="strong-pass-123")

        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="jane@example.com", password="another-pass-123")
