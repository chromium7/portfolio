from datetime import date

from django.test import TestCase
from django.urls import reverse

from portfolio.apps.events.models import Event, EventCategory


class EventsViewTest(TestCase):
    def setUp(self) -> None:
        self.category = EventCategory.objects.create(name="Marathon", group=EventCategory.Group.RUNNING)

    def test_events_page_renders(self) -> None:
        response = self.client.get(reverse("pages:events"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/events.html")
        self.assertContains(response, "Events")

    def test_events_page_empty_state(self) -> None:
        response = self.client.get(reverse("pages:events"))
        self.assertContains(response, "No events yet")

    def test_events_page_with_data(self) -> None:
        Event.objects.create(
            name="Jakarta Marathon",
            category=self.category,
            date=date(2025, 10, 26),
            location="Jakarta, ID",
            notes="First full marathon.",
        )
        response = self.client.get(reverse("pages:events"))
        self.assertContains(response, "Jakarta Marathon")
        self.assertContains(response, "Oct 2025")
        self.assertContains(response, "Jakarta, ID")
        self.assertContains(response, "First full marathon.")

    def test_events_page_category_filter_buttons(self) -> None:
        cat_ultra = EventCategory.objects.create(name="Ultra", group=EventCategory.Group.RUNNING)
        Event.objects.create(name="Ultra Run", category=cat_ultra, date=date(2025, 6, 1))
        Event.objects.create(name="Marathon", category=self.category, date=date(2025, 10, 26))
        response = self.client.get(reverse("pages:events"))
        self.assertContains(response, 'data-filter="Marathon"')
        self.assertContains(response, 'data-filter="Ultra"')

    def test_events_page_with_urls(self) -> None:
        Event.objects.create(
            name="Strava Event",
            category=self.category,
            date=date(2025, 1, 1),
            strava_url="https://www.strava.com/activities/123",
            official_result_url="https://results.example.com/456",
        )
        response = self.client.get(reverse("pages:events"))
        self.assertContains(response, "Strava ↗")
        self.assertContains(response, "Results ↗")

    def test_events_page_ordering(self) -> None:
        Event.objects.create(name="Older", category=self.category, date=date(2024, 1, 1))
        Event.objects.create(name="Newer", category=self.category, date=date(2025, 12, 31))
        response = self.client.get(reverse("pages:events"))
        content = response.content.decode()
        newer_pos = content.index("Newer")
        older_pos = content.index("Older")
        self.assertLess(newer_pos, older_pos)
