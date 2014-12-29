from django.shortcuts import render
from django.views.generic import DetailView, ListView

from races.models import Race, Season


class RaceDetailView(DetailView):
    """ Displays details for a specific race. """
    model = Race
    template_name = 'races/race_detail.html'

    def get_context_data(self, **kwargs):
        "Adds current season into context"
        context = super(RaceDetailView, self).get_context_data(**kwargs)
        context['current_season'] = Season.current_season.all()
        return context


class CurrentSeasonRaceListView(DetailView):
    """ Displays races for a given season. """
    model = Season
    template_name = 'races/current_season_race_list.html'

    def get_context_data(self, **kwargs):
        "Adds race list for season into context"
        context = super(CurrentSeasonRaceListView, self).get_context_data(**kwargs)
        context['race_list'] = Race.objects.filter(season__slug=self.kwargs['slug'])
        return context
