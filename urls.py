from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'kushillu.views.page_with_ajax', name='build-list', kwargs={'ajax_url': 'build-list-ajax'}),
    url(r'^ajax/$', 'kushillu.views.build_list_ajax', name='build-list-ajax'),

    url(r'^(?P<pk>\d+)/$', 'kushillu.views.page_with_ajax', name='build-details', kwargs={'ajax_url': 'build-details-ajax'}),
    url(r'^ajax/(?P<pk>\d+)/$', 'kushillu.views.build_details_ajax', name='build-details-ajax'),

    url(r'^build/manual/$', 'kushillu.views.go_build', name='go-build'),

    url(r'^project/(?P<pk>\d+)/webhook$', 'kushillu.views.webhook', name='webhook'),
    url(r'^project/(?P<pk>\d+)/status.svg$', 'kushillu.views.status_svg', name='status-svg'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.jinja'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
