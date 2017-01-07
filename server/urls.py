from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'server'

urlpatterns = [
    url(r'^add_user', views.add_user, name='add_user'),
    url(r'^login', views.user_login, name='login'),
    url(r'^hello/$', views.hello.as_view()),
    url(r'^hello/(?P<pk>[0-9]+)/$', views.snippet_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)