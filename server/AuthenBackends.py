from .models import User

class FBBackend():
    def authenticate(self, fb_id):
        try:
            return User.objects.get(fb_id=fb_id)
        except User.DoesNotExist:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_staff()