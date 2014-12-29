from django.views.generic import TemplateView

from races.models import Race, Season


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['weekend_race_list'] = Race.upcoming_races_for_weekend.all()
        context['remaining_races_for_month_list'] = Race.upcoming_races_for_month.all()
        context['current_season'] = Season.current_season.all()
        return context
