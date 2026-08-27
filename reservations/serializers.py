from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Artist, Show


class ArtistSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'firstname', 'lastname', 'links']

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse('reservations:artist-api-detail', kwargs={'pk': obj.id}, request=request),
            'all_artists': reverse('reservations:artist-api-list', request=request),
        }


class ShowSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'title', 'description', 'duration', 'bookable', 'price', 'links']

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse('reservations:show-api-detail', kwargs={'pk': obj.id}, request=request),
            'all_shows': reverse('reservations:show-api-list', request=request),
        }
