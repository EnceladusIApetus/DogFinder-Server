from __future__ import unicode_literals
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from DogFinderServer import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Coordinate(models.Model):
    name = models.CharField(max_length=30, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    path = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    path = models.FileField(upload_to='files/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Dog(models.Model):
    name = models.CharField(max_length=30)
    breed = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='dog_set')
    note = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, default=0.0)
    longitude = models.FloatField(null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_images(self):
        images = []
        for instance in self.instance_set.all():
            images.append(instance.image.path.url)
        return images


class Instance(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    raw_features = models.TextField(null=True)
    reduced_features = models.TextField(null=True)
    label = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DogLocation(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    coordinate = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DogStatus(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.IntegerField()
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, fb_id, fb_name, fb_token, fb_token_exp, email, telephone, birth_date, password=None):
        # type: (object, object, object, object, object, object, object, object) -> object
        user = self.model(fb_id=fb_id, fb_name=fb_name, fb_token=fb_token, fb_token_exp=fb_token_exp, email=email, telephone=telephone, birth_date=birth_date)
        user.save(using=self._db)
        return user

    def create_superuser(self, fb_id, fb_name, fb_token, fb_token_exp, email, telephone, birth_date, password=None):
        user = self.create_user(fb_id, fb_name, fb_token, fb_token_exp, email, telephone, birth_date)
        user.role = 1
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    fb_id = models.CharField(max_length=30, unique=True)
    fb_name = models.CharField(max_length=100)
    fb_token = models.TextField()
    fb_token_exp = models.DateTimeField(blank=True, null=True)
    fb_profile_image = models.TextField(default=None)
    role = models.IntegerField(default=1)
    email = models.CharField(max_length=50, null=True)
    telephone = models.CharField(max_length=20, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'fb_id'
    REQUIRED_FIELDS = ['fb_name', 'fb_token', 'fb_token_exp', 'fb_profile_image']

    def is_active(self):
        return self.active

    def get_full_name(self):
        return self.fb_id

    def get_short_name(self):
        return self.fb_id

    def set_active(self):
        self.active = True
        self.save()

    def set_inactive(self):
        self.active = False
        self.save()

    @property
    def is_staff(self):
        return True if self.role == 0 else False

    def has_perm(self, perm, obj=None):
        if self.is_staff:
            return True
        elif perm == 'manage_own_dog':
            return True if obj.user == self else False

    def has_module_perms(self, app_label):
        return self.is_staff()


class LostAndFound(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    type = models.IntegerField()
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    LOST = 0
    FOUND = 1


class LocationImg(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    lost_and_found = models.ForeignKey(LostAndFound, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    lost_and_found = models.ForeignKey(LostAndFound, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lost_and_found = models.ForeignKey(LostAndFound, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


