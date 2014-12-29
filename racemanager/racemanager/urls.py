from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from homepage.views import HomePageView
from races.views import RaceDetailView, CurrentSeasonRaceListView

admin.site.header = 'NCCX administration'

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^seasons/(?P<slug>[\w-]+)/$', CurrentSeasonRaceListView.as_view(), name='current_season_race_list'),
    url(r'^races/(?P<pk>\d+)/$', RaceDetailView.as_view(), name='race_detail'),
    url(r'^administration/', include(admin.site.urls)),
    url(r'^administration/doc/', include('django.contrib.admindocs.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
