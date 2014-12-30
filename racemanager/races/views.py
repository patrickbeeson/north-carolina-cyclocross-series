from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

from races.models import Race, Season


class RaceDetailView(DetailView):
    """
    Displays details for a specific race.
    """
    context_object_name = 'race'
    model = Race
    template_name = 'races/race_detail.html'

    def get_queryset(self):
        self.season = get_object_or_404(Season, slug=self.kwargs['slug'])
        return Race.objects.filter(season=self.season)

    def get_context_data(self, **kwargs):
        "Adds current season into context"
        context = super(RaceDetailView, self).get_context_data(**kwargs)
        context['season'] = Season.current_season.all()
        return context


class CurrentSeasonRaceListView(ListView):
    """
    Displays races for a given season.
    """
    context_object_name = 'race_list'
    template_name = 'races/current_season_race_list.html'

    def get_queryset(self):
        self.season = get_object_or_404(Season, slug=self.kwargs['slug'])
        return Race.objects.filter(season=self.season)

    def get_context_data(self, **kwargs):
        context = super(CurrentSeasonRaceListView, self).get_context_data(**kwargs)
        context['season'] = self.season
        return context
