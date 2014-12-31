from django.views.generic import TemplateView

from races.models import Race, Season


class HomePageView(TemplateView):
    """
    Homepage view
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        "Add context to homepage for upcoming races and seasonal information."
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['weekend_race_list'] = Race.upcoming_races_for_weekend.all()
        context['remaining_races_for_month_list'] = Race.upcoming_races_for_month.all()
        context['upcoming_races_for_next_month_list'] = Race.upcoming_races_for_next_month.all()
        context['season'] = Season.current_season.all()
        return context
