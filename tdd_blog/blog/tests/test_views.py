from django.test import TestCase
from django.contrib.auth import get_user_model
from django.template import Template, Context
from django_webtest import WebTest
from blog.models import Entry, Comment
from django.template.defaultfilters import slugify
import datetime


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


class EntryViewDetailTest(WebTest):
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

    def test_no_comments_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, "There are no comments yet.")

    def test_single_comment_in_entry(self):
        comment = Comment.objects.create(
            entry=self.entry, name="test", body="some test"
        )
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, comment.body)

    def test_two_comments_in_entry(self):
        comment1 = Comment.objects.create(
            entry=self.entry, name="test1", body="some test1"
        )
        comment2 = Comment.objects.create(
            entry=self.entry, name="test2", body="some test2"
        )
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, comment1.body)
        self.assertContains(response, comment2.body)

    def test_view_page(self):
        page = self.app.get(self.entry.get_absolute_url())
        self.assertEqual(len(page.forms), 1)

    def test_form_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.entry.get_absolute_url())
        page.form["name"] = "Philip"
        page.form["email"] = "philipp2@hotmail.com"
        page.form["body"] = "some test form text"
        page = page.form.submit()
        self.assertRedirects(page, self.entry.get_absolute_url())


class EntryViewUrlTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.entry = Entry.objects.create(title="title", body="body", author=self.user)

    def test_url(self):
        title = "my test title"
        today = datetime.date.today()
        entry = Entry.objects.create(title=title, body="body", author=self.user)
        test_slug = slugify(title)
        url = "/blog/{year}/{month}/{day}/{pk}-{slug}/".format(
            year=today.year,
            month=today.month,
            day=today.day,
            pk=entry.pk,
            slug=test_slug,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="blog/entry_detail.html")

    def test_missdated_url(self):
        url = "/blog/0000/00/00/{0}-misdated/".format(self.entry.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="blog/entry_detail.html")

    def test_invalid_url(self):
        response = self.client.get("/blog/0000/00/00/0-invalid-url/")
        self.assertEqual(response.status_code, 404)


class EntryHistoryTagTest(TestCase):

    TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

    def setUp(self):
        self.user = get_user_model().objects.create(username="test")

    def test_entry_show_up(self):
        entry = Entry.objects.create(title="Some title", author=self.user)
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn(entry.title, rendered)

    def test_no_recent_entries(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("There are no recent entries yet.", rendered)

    def test_show_many_entries(self):
        for i in range(1, 6):
            Entry.objects.create(title=f"Post {i}", author=self.user)
        rendered = self.TEMPLATE.render(Context({}))
        for i in range(1, 6):
            self.assertIn(f"Post {i}", rendered)
        self.assertNotIn("Post 8", rendered)
