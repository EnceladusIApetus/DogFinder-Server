from rest_framework import serializers
import models


class CoordinateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = models.Coordinate
        fields = ('id', 'name', 'latitude', 'longitude', 'created_at')