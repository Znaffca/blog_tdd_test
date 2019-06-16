from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords


class Entry(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    objects = models.Manager()

    @property
    def shorten_body(self):
        return truncatewords(self.body, 20)

    def get_absolute_url(self):
        return reverse("blog:entry_detail", args=(self.pk,))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Entries"


class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.body
