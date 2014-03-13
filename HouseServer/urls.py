from django.conf.urls import patterns, include, url

from django.contrib import admin

import accounts

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HouseServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include('accounts.urls')),

    url(r'^survey/', include('survey.urls', namespace="survey")),

)
