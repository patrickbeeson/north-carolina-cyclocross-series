from django.shortcuts import render
from django.views.generic import DetailView, ListView

from races.models import Race, Season


class RaceDetail(DetailView):
    model = Race


class CurrentSeasonRaceList(DetailView):
    model = Season
    queryset = Season.current_season.all()
    template_name = 'upcoming_race_list.html'


class ResultsList(ListView):
    model = Season
