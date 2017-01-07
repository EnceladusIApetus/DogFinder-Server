from __future__ import unicode_literals
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from DogFinderServer import settings


class Coordinate(models.Model):
    name = models.CharField(max_length=30, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    name = models.CharField(max_length=30, null=True)
    path = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Dog(models.Model):
    name = models.CharField(max_length=30)
    bleed = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uodated_at = models.DateTimeField(auto_now=True)


class Instance(models.Model):
    dog_id = models.ForeignKey(Dog, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    original_features = models.TextField(null=True)
    reduced_features = models.TextField(null=True)
    label = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DogLocation(models.Model):
    dog_id = models.ForeignKey(Dog, on_delete=models.CASCADE)
    coordinate_id = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DogStatus(models.Model):
    dog_id = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.IntegerField()
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, fb_id, fb_name, fb_token, fb_token_exp, email, telephone, birth_date, password=None):
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
    role = models.IntegerField(default=1)
    email = models.CharField(max_length=50, null=True)
    telephone = models.CharField(max_length=20, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'fb_id'
    REQUIRED_FIELDS = ['email']

    def is_active(self):
        return self.active

    def get_full_name(self):
        return self.fb_id

    def get_short_name(self):
        return self.fb_id

    @property
    def is_staff(self):
        return True if self.role == 0 else False

    def has_perm(self, perm, obj=None):
        return self.is_staff()

    def has_module_perms(self, app_label):
        return self.is_staff()


class LostAndFound(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    dog_id = models.ForeignKey(Dog, on_delete=models.CASCADE)
    type = models.IntegerField()
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LocationImg(models.Model):
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    lost_and_found = models.ForeignKey(LostAndFound, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    lost_and_found_id = models.ForeignKey(LostAndFound, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




