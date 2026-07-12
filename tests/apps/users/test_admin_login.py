from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminLoginTests(TestCase):
    def setUp(self) -> None:
        self.password = "strong-pass-123"
        self.staff_user = User.objects.create_user(
            email="staff@example.com",
            password=self.password,
            is_staff=True,
        )

    def test_login_flow(self) -> None:
        login_url = reverse("admin:login")

        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            login_url,
            data={"username": "staff@example.com", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        response = self.client.post(
            login_url,
            data={"username": "staff@example.com", "password": self.password},
            follow=True,
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.staff_user)

    def test_inactive_user_cannot_log_in(self) -> None:
        self.staff_user.is_active = False
        self.staff_user.save(update_fields=["is_active"])

        logged_in = self.client.login(username="staff@example.com", password=self.password)

        self.assertFalse(logged_in)
