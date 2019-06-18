from django.test import TestCase
from blog.models import Entry, Comment
from blog.forms import CommentForm
from django.contrib.auth import get_user_model


class CommentFormTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="grzegorz")
        self.entry = Entry.objects.create(author=user, title="Sample test title")

    def test_init_form(self):
        CommentForm(entry=self.entry)

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()

    def test_valid_data(self):
        form = CommentForm(
            {"name": "test", "email": "test@test.gov", "body": "some body"},
            entry=self.entry,
        )
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "test")
        self.assertEqual(comment.email, "test@test.gov")
        self.assertEqual(comment.body, "some body")
        self.assertEqual(comment.entry, self.entry)

    def test_blank_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "name": ["This field is required."],
                "email": ["This field is required."],
                "body": ["This field is required."],
            },
        )
