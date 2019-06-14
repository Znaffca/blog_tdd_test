from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", views.HomeView.as_view(), name="home"),
    re_path(r"^(?P<pk>\d+)/$", views.EntryDetailView.as_view(), name="entry_detail"),
]
