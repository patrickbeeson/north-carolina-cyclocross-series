from django.conf.urls import patterns, include, url

from races.views import RaceDetailView, CurrentSeasonRaceListView, SeasonListView, CurrentSeasonRaceResultsListView


urlpatterns = patterns('',
    url(
        r'^$',
        SeasonListView.as_view(),
        name='season_list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        CurrentSeasonRaceListView.as_view(),
        name='current_season_race_list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/past-races-and-results/$',
        CurrentSeasonRaceResultsListView.as_view(),
        name='current_season_past_race_list'
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$',
        RaceDetailView.as_view(),
        name='race_detail'
    ),
)
