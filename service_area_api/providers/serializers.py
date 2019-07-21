from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Provider, ServiceArea


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'url', 'name', 'email', 'phone_number',
                  'language', 'currency', 'created_at', 'updated_at')


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = ProviderSerializer(read_only=True)
    class Meta:
        model = ServiceArea
        fields = ('id', 'url', 'name', 'price', 'provider',
                  'polygon', 'created_at', 'updated_at')
        geo_field = 'polygon'