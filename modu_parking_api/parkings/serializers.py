from rest_framework import serializers
from lots.serializers import LotsSerializer
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    """Parking create, delete, detail Serializer
    Create:
    request = lot, parking_time
    response = id, lot(foreign), start_time, parking_time

    Detail - only the user's parking history can be viewed:
    response = id, lot(foreign), start_time, parking_time

    Delete:
    response = 204
    """

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'start_time',
            'parking_time',
            'user',
        )
        read_only_fields = ('id', 'start_time', 'user')


class ParkingUpdateSerializer(serializers.ModelSerializer):
    """
    Update:
    request = additional_time
    response = id, lot(foreign), start_time, parking_time
    """
    lot = LotsSerializer()

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'start_time',
            'parking_time',
        )
        read_only_fields = ('id', 'lot', 'start_time', 'parking_time',)


class ParkingListSerializer(serializers.ModelSerializer):
    """
    List - the user's parking history:
    response = id, lot(foreign), parking_time
    """
    lot = LotsSerializer()

    class Meta:
        model = Parking
        fields = (
            'id',
            'lot',
            'parking_time'
        )