from rest_framework import serializers
from lots.models import Lot


class LotsSerializer(serializers.ModelSerializer):
    """ Create, Update, Detail view serializer """
    class Meta:
        model = Lot
        fields = ['name', 'address', 'latitude', 'longitude', 'basic_rate', 'additional_rate',
                  'time_weekdays', 'time_weekends', 'section_count', ]


class MapSerializer(serializers.ModelSerializer):
    """ List view : Filtering by zoom level and coordinates on the map"""
    class Meta:
        model = Lot
        fields = ['id', 'latitude', 'longitude', 'basic_rate', ]


