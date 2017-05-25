from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from server.views import device
from server.views import general
from .views import user, test, dogs

app_name = 'server'


urlpatterns = [
    url(r'^user/login$', user.UserAuthentication.UserLogin.as_view(), name='login'),
    url(r'^user/logout$', user.UserAuthentication.UserLogout.as_view(), name='logout'),
    url(r'^user/is_authenticate', user.UserAuthentication.IsAuthenticate.as_view(), name='is_authenticate'),
    url(r'^user/self$', user.UserData.SelfInfo.as_view(), name='self_info'),
    url(r'^user/get_user$', user.UserData.GetUser.as_view(), name='user_info'),
    url(r'^upload/file$', general.UploadFile.as_view(), name="upload_file"),
    url(r'^upload/image$', general.UploadImage.as_view(), name="upload_image"),
    url(r'^dog/instance$', dogs.Instance.as_view()),
    url(r'^dog/get_all_dogs', dogs.GetAllDog.as_view()),
    url(r'^dog/add_dog_samples$', dogs.AddDogSamples.as_view()),
    url(r'^dog/find_similar_dogs', dogs.FindSimilarDogs.as_view()),
    url(r'^dog/lost_and_found', dogs.LostAndFoundAPI.as_view()),
    url(r'^dog/gen_lost_and_found', dogs.GenLostAndFound.as_view()),
    url(r'^dog/reduce_features', dogs.ReduceFeature.as_view()),
    url(r'^dog/$', dogs.Individual.as_view()),
    url(r'^device/fcm_token', device.UpdateFCMToken.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)