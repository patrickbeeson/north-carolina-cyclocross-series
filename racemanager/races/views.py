from django.shortcuts import render
from django.views.generic import DetailView

from races.models import Race


class RaceDetail(DetailView):
    model = Race
