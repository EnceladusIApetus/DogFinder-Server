from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import datetime


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text
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



class User(AbstractBaseUser):
    fb_id = models.CharField(max_length=30, unique=True)
    fb_name = models.CharField(max_length=100)
    fb_token = models.TextField()
    fb_token_exp = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=50, null=True)
    telephone = models.CharField(max_length=20, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'fb_id'
    REQUIRED_FIELDS = ['email']


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




