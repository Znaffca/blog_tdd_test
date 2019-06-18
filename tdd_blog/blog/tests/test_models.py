from django.test import TestCase
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatewords
from blog.models import Entry, Comment


class EntryModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="some_user")

    def test_string_representation(self):
        entry = Entry(title="my entry title")
        self.assertEqual(str(entry), entry.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "Entries")

    def test_get_absolute_url(self):
        entry = Entry.objects.create(title="my entry title", author=self.user)
        self.assertIsNotNone(entry.get_absolute_url())

    def test_entry_shorten_body_with_long_body_text(self):
        entry = Entry.objects.create(
            body="aa aa aa aa aa aa aa aa aa aa aa aa aa aa aa aa aa aaa aa aa aa aa aa aa aa",
            author=self.user,
        )
        self.assertEqual(entry.shorten_body, truncatewords(entry.body, 20))

    def test_entry_shorten_body_with_short_body_text(self):
        entry = Entry.objects.create(body="short body", author=self.user)
        self.assertEqual(entry.shorten_body, entry.body)


class CommentModelTest(TestCase):
    def test_comment_representation(self):
        comment = Comment(
            name="greg", email="greg@gmail.com", body="Some b****it is here "
        )
        self.assertEqual(str(comment), comment.body)
