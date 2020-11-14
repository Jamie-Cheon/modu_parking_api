from rest_framework import serializers
from lots.models import Lot


class LotsSerializer(serializers.ModelSerializer):
    """create, update, detail"""
    class Meta:
        model = Lot
        fields = ['name', 'address', 'latitude', 'longitude', 'basic_rate', 'additional_rate',
                  'time_weekdays', 'time_weekends', 'section_count', ]


class MapSerializer(serializers.ModelSerializer):
    """list : filtering by zoom-lv and coordinates"""
    class Meta:
        model = Lot
        fields = ['id', 'latitude', 'longitude', 'basic_rate', ]


"""
lots app
POST /lots/
PUT /lots/id
GET /lots/id
DELETE /lots/id 

GET /lots/map(action) 
"""

