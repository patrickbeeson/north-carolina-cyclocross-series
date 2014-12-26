from django.views.generic import TemplateView

from races.models import Races


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['race_list'] = Race.upcoming_races.all()
        context['weekend_race_list'] = Race.upcoming_races_for_weekend.all()
        context['remaining_races_for_month_list'] = Race.upcoming_races_for_month.all()
        # Need to add context for results, model too?
