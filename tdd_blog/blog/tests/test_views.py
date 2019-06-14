from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Entry


class ProjectViewInitialTest(TestCase):
    def test_default_address(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 404)

    def test_blog_address(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)


class HomePageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")

    def test_one_entry(self):
        Entry.objects.create(title="1-title", body="1-body", author=self.user)
        response = self.client.get("/blog/")
        self.assertContains(response, "1-title")
        self.assertContains(response, "1-body")

    def test_two_entries(self):
        Entry.objects.create(title="1-title", body="1-body", author=self.user)
        Entry.objects.create(title="2-title", body="2-body", author=self.user)
        response = self.client.get("/blog/")
        self.assertContains(response, "1-title")
        self.assertContains(response, "1-body")
        self.assertContains(response, "2-title")

    def test_no_entries(self):
        response = self.client.get("/blog/")
        self.assertContains(response, "There are no blog entries yet.")


class EntryViewDetailTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="Skipper")
        self.entry = Entry.objects.create(
            title="What is going", body="gimme options", author=self.user
        )

    def test_basic_view(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_title_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.title)
        self.assertContains(response, self.entry.body)
