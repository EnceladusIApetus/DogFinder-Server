from django.conf.urls import url

from . import views

app_name = 'server'
urlpatterns = [
    url(r'^add_user', views.add_user, name='add_user'),
    url(r'^login', views.user_login, name='login'),
    url(r'^hello', views.hello),
]