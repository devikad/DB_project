from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'myapp.views.index'),  # root
    url(r'^login$', 'myapp.views.login_view'),  # login
    url(r'^logout$', 'myapp.views.logout_view'),  # logout
    url(r'^signup$', 'myapp.views.signup'),  # signup
    url(r'^submit$', 'myapp.views.submit_comments'),  # submit new comment
    url(r'^groups/(?P<usergroup_id>\d+)/$', 'myapp.views.usergroup_view'),  # groups
    url(r'^joingroup/(?P<usergroup_id>\d+)/$', 'myapp.views.join_group'),  # join the group
    url(r'^search_form/$', 'myapp.views.search_view'),
    url(r'^profile/(?P<user_id>\d+)/$', 'myapp.views.profile'),  # profile
    url(r'^university/(?P<uni_id>\d+)/$', 'myapp.views.university'),  # uni
    url(r'^company/(?P<comp_id>\d+)/$', 'myapp.views.company'),  # comp
)

