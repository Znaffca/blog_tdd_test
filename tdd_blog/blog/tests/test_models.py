from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Entry


class EntryModelTest(TestCase):
    def test_string_representation(self):
        entry = Entry(title="my entry title")
        self.assertEqual(str(entry), entry.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "Entries")

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username="some_user")
        entry = Entry.objects.create(title="my entry title", author=user)
        self.assertIsNotNone(entry.get_absolute_url())
