from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.shortcuts import get_object_or_404

from races.models import Race, Season

class CurrentSeasonMixin(ContextMixin):
    """
    Adds current season context as a mixin.
    """

    def get_context_data(self, **kwargs):
        "Adds the current season into context."
        context = super(CurrentSeasonMixin, self).get_context_data(**kwargs)
        context['season'] = Season.current_season.all()
        return context


class RaceDetailView(CurrentSeasonMixin, DetailView):
    """
    Displays details for a specific race.
    """
    context_object_name = 'race'
    template_name = 'races/race_detail.html'

    def get_queryset(self):
        "Filters the queryset for races in a season."
        self.season = get_object_or_404(Season, slug=self.kwargs['slug'])
        return Race.objects.filter(season=self.season)


class SeasonListView(CurrentSeasonMixin, ListView):
    """
    Displays a list of all seasons, current and past.
    """
    context_object_name = 'season_list'
    template_name = 'races/season_list.html'
    queryset = Season.objects.all()



class CurrentSeasonRaceListView(CurrentSeasonMixin, ListView):
    """
    Displays races for a given season.
    """
    context_object_name = 'race_list'
    template_name = 'races/current_season_race_list.html'

    def get_queryset(self):
        "Filters the queryset for races in a season."
        self.season = get_object_or_404(Season, slug=self.kwargs['slug'])
        return Race.objects.filter(season=self.season)
