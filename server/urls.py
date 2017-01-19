from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from server.views import general
from .views import user, test, dogs

app_name = 'server'

urlpatterns = [
    url(r'^user/login$', user.UserAuthentication.UserLogin.as_view(), name='login'),
    url(r'^user/logout$', user.UserAuthentication.UserLogout.as_view(), name='logout'),
    url(r'^user/is_authenticate', user.UserAuthentication.IsAuthenticate.as_view(), name='is_authenticate'),
    url(r'^user/self$', user.UserData.SelfInfo.as_view(), name='self_info'),
    url(r'^user/get_user$', user.UserData.GetUser.as_view(), name='user_info'),
    url(r'^hello/$', test.hello.as_view()),
    url(r'^hello/(?P<pk>[0-9]+)/$', test.snippet_detail.as_view()),
    url(r'^upload/file$', general.UploadFile.as_view(), name="upload_file"),
    url(r'^upload/image$', general.UploadImage.as_view(), name="upload_image"),
    url(r'^dog$', dogs.IndividualDog.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)