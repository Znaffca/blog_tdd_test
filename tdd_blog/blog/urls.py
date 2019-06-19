from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^$", views.HomeView.as_view(), name="home"),
    # re_path(r"^(?P<pk>\d+)/$", views.EntryDetailView.as_view(), name="entry_detail"), -> old url replaced
    re_path(r"^(?P<year>\d{4})\/(?P<month>\d{1,2})\/(?P<day>\d{1,2})\/(?P<pk>\d+)-(?P<slug>[-\w]*)\/$", views.EntryDetailView.as_view(), name="entry_detail"),
    # path("<int:year>/<int:month>/<int:day>/<int:pk>-<slug:slug>/", views.EntryDetailView.as_view(), name="entry_detail"), 
]
