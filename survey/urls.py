import views

from django.conf.urls import patterns, url

#Define URLs here
urlpatterns = patterns(
    # /index/
    url(r'^index/$', views.index, name='index1'),

    # /instrument/1/sort/6/
    url(r'^instrument/(?P<id>\d+)/sort/(?P<sort>\d+)/$', views.instrumentDetail, name="InstrumentDetailed"),
    # /instrument/1/
    url(r'^instrument/(?P<id>\d+)/$', views.instrumentDetail, name="InstrumentDetailed"),
    # /instrument/
    url(r'^instrument/$', views.instrument, name='InstrumentAll'),

    # /stamp/sort/6
    url(r'^stamp/sort/(?P<sort>\d+)/$', views.timestamp, name="TimestampInterval"),
    # /stamp/1
    url(r'^stamp/detail/(?P<id>\d+)/$', views.timestampDetail, name="TimestampDetailed"),
    # /stamp/find/<y>/<mo>/<d>/<h>/<mi>/
    url(r'stamp/find/$', views.find, name="TimeStampfind"),
    # /stamp/
    url(r'^stamp/$', views.timestamp, name="TimestampGeneral"),

    # /generate/
    url(r'^generate/', views.generate, name="generate"),

    # /download/10/144/
    url(r'^download/(?P<amount>\d+)/(?P<interval>\d+)/$', views.download, name="Download2"),
    # /download/
    url(r'^download/$', views.download, name="Download"),
    # /
    url(r'^$', views.index, name='index'),
)