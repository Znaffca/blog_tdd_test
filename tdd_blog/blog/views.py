# from django.shortcuts import render
from django.views.generic import ListView
from .models import Entry


class HomeView(ListView):
    template_name = 'blog/index.html'
    queryset = Entry.objects.order_by('-created')
