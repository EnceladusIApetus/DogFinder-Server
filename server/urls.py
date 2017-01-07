from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import user

app_name = 'server'

urlpatterns = [
    url(r'^login', user.user_login, name='login'),
    url(r'^logout', user.user_logout, name='logout'),
    url(r'^hello/$', views.hello.as_view()),
    url(r'^hello/(?P<pk>[0-9]+)/$', views.snippet_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)