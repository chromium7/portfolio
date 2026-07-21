from datetime import date
from decimal import Decimal

from django.test import TestCase

from portfolio.apps.events.models import Event, EventCategory


class EventCategoryModelTest(TestCase):
    def test_auto_slug_on_save(self) -> None:
        category = EventCategory.objects.create(name="Half Marathon")
        self.assertEqual(category.slug, "half-marathon")

    def test_str(self) -> None:
        category = EventCategory.objects.create(name="Marathon")
        self.assertEqual(str(category), "Marathon")

    def test_ordering(self) -> None:
        cat1 = EventCategory.objects.create(name="10K", group=EventCategory.Group.RUNNING)
        cat2 = EventCategory.objects.create(name="5K", group=EventCategory.Group.RUNNING)
        cats = list(EventCategory.objects.all())
        self.assertEqual(cats[0], cat1)
        self.assertEqual(cats[1], cat2)

    def test_default_group(self) -> None:
        category = EventCategory.objects.create(name="Tennis Tournament")
        self.assertEqual(category.group, EventCategory.Group.OTHER)

    def test_create_event_category(self) -> None:
        category = EventCategory.objects.create(
            name="Half Marathon",
            slug="half-marathon",
            group=EventCategory.Group.RUNNING,
            typical_distance_km=Decimal("21.10"),
        )
        self.assertEqual(category.name, "Half Marathon")
        self.assertEqual(category.slug, "half-marathon")
        self.assertEqual(category.group, EventCategory.Group.RUNNING)
        self.assertEqual(category.typical_distance_km, Decimal("21.10"))
        self.assertEqual(str(category), "Half Marathon")


class EventModelTest(TestCase):
    def setUp(self) -> None:
        self.category = EventCategory.objects.create(name="Marathon", group=EventCategory.Group.RUNNING)

    def test_str(self) -> None:
        event = Event.objects.create(name="Jakarta Marathon", category=self.category, date=date(2025, 10, 26))
        self.assertIn("Jakarta Marathon", str(event))
        self.assertIn("2025", str(event))

    def test_string_representation(self) -> None:
        event = Event.objects.create(name="Test Run", category=self.category, date=date(2025, 1, 1))
        self.assertEqual(str(event), "Test Run (2025)")

    def test_default_result_type(self) -> None:
        event = Event.objects.create(name="Test Run", category=self.category, date=date(2025, 1, 1))
        self.assertEqual(event.result_type, Event.ResultType.TIME)

    def test_ordering_desc_date(self) -> None:
        e1 = Event.objects.create(name="Older", category=self.category, date=date(2025, 1, 1))
        e2 = Event.objects.create(name="Newer", category=self.category, date=date(2025, 12, 31))
        events = list(Event.objects.all())
        self.assertEqual(events[0], e2)
        self.assertEqual(events[1], e1)

    def test_create_event(self) -> None:
        event = Event.objects.create(
            name="Jakarta Half Marathon 2026",
            category=self.category,
            date=date(2026, 3, 15),
            location="Jakarta, Indonesia",
            result_type=Event.ResultType.TIME,
            distance_km=Decimal("21.10"),
            finish_time="1:45:30",
            bib_number="1234",
        )
        self.assertEqual(event.name, "Jakarta Half Marathon 2026")
        self.assertEqual(event.location, "Jakarta, Indonesia")
        self.assertEqual(event.distance_km, Decimal("21.10"))
        self.assertEqual(str(event), "Jakarta Half Marathon 2026 (2026)")
