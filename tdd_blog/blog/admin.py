from django.contrib import admin
from .models import Entry, Comment

# Register your models here.


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "shorten_body", "created", "modified")
    list_filter = ("author", "created", "modified")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    ordering = ("created", "modified")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("entry", "name", "email", "body", "created", "updated")
    list_filter = ("created", "updated")
    search_fields = ("name", "email", "body")
    ordering = ("created", "updated")
