from rest_framework import serializers
import models


class BasicAccountSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.User
        fields = ('fb_name', 'fb_profile_image', 'email', 'telephone', 'birth_date', 'created_at', 'updated_at',)


class DogSerializer(serializers.ModelSerializer):
    user = BasicAccountSerializer(read_only=True, required=False)
    images = serializers.ListField(source='get_images', read_only=True)
    age = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    breed = serializers.CharField(required=False)
    longitude = serializers.FloatField(required=False)
    latitude = serializers.FloatField(required=False)
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    def create(self):
        return models.Dog(**self.validated_data)

    class Meta:
        model = models.Dog
        fields = ('id', 'name', 'breed', 'age', 'user', 'note', 'images', 'longitude', 'latitude', 'created_at', 'updated_at')


class FullAccountSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    def update(self, instance, validated_data):
        instance.fb_name = validated_data.get('fb_name', instance.fb_name)
        instance.fb_token = validated_data.get('fb_token', instance.fb_token)
        instance.fb_token_exp = validated_data.get('fb_token_exp', instance.fb_token_exp)
        instance.fb_profile_image = validated_data.get('fb_profile_image', instance.fb_profile_image)
        instance.email = validated_data.get('email', instance.email)
        instance.telephone = validated_data.get('telephone', instance.telephone)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance

    class Meta:
        model = models.User
        read_only_fields = ('id',)
        fields = ('id', 'fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'fb_profile_image', 'email', 'telephone', 'birth_date', 'created_at', 'updated_at',)


class CoordinateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.Coordinate
        fields = ('id', 'name', 'latitude', 'longitude', 'created_at')


class ImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.Image
        fields = ('name', 'path', 'created_at')


class InstanceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.Instance
        fields = ('dog_id', 'image_id', 'raw_features', 'reduced_features', 'label', 'created_at', 'updated_at')


class DogLocationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.DogLocation
        fields = ('dog_id', 'coordinate_id', 'name', 'created_at')


class DogStatusSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.DogStatus
        fields = ('dog_id', 'status', 'note', 'created_at')


class LostAndFoundSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)
    dog = DogSerializer()
    class Meta:
        model = models.LostAndFound
        fields = ('dog', 'type', 'note', 'created_at', 'updated_at')


class LocationImgSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.LocationImg
        fields = ('image_id', 'lost_and_found_id', 'created_at')


class ChatSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.LocationImg
        fields = ('user_id', 'lost_and_found_id', 'message', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = ('user_id', 'lost_and_found_id', 'created_at')