from rest_framework import serializers
import models


class CoordinateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.Coordinate
        fields = ('id', 'name', 'latitude', 'longitude', 'created_at')


class ImageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.Image
        fields = ('name', 'path', 'created_at')


class DogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.Dog
        fields = ('name', 'bleed', 'age', 'owner', 'note', 'created_at', 'updated_at')


class InstanceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.Instance
        fields = ('dog_id', 'image_id', 'raw_features', 'reduced_features', 'label', 'created_at', 'updated_at')


class DogLocationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.DogLocation
        fields = ('dog_id', 'coordinate_id', 'name', 'created_at')


class DogStatusSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.DogStatus
        fields = ('dog_id', 'status', 'note', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.User
        fields = ('fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'email', 'telephone', 'birth_date', 'created_at', 'updated_at')


class LostAndFoundSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.LostAndFound
        fields = ('user_id', 'dog_id', 'type', 'note', 'created_at', 'updated_at')


class LocationImgSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.LocationImg
        fields = ('image_id', 'lost_and_found_id', 'created_at')


class ChatSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        models = models.LocationImg
        fields = ('user_id', 'lost_and_found_id', 'message', 'created_at')
