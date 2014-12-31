from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from homepage.views import HomePageView

admin.site.header = 'NCCX administration'

urlpatterns = patterns('',
    url(
        r'^$',
        HomePageView.as_view(),
        name='home'
    ),
    url(
        r'^races/',
        include('races.urls', namespace='races'),
    ),
    url(
        r'^administration/',
        include(admin.site.urls)
    ),
    url(
        r'^administration/doc/',
        include('django.contrib.admindocs.urls')
    ),
    # url(
    #     r'^pages/',
    #     include('django.contrib.flatpages.urls')
    # ),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += patterns('django.contrib.flatpages.views',
#     (r'^(?P<url>.*/)$', 'flatpage'),
# )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
