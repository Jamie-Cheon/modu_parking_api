from rest_framework import serializers
from lots.serializers import LotsSerializer
from parkings.models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    """create, delete, detail
    create:
    request = lot, parking_time
    response = id, lot(foreign), start_time, parking_time
    detail(login required):
    response = id, lot(foreign), start_time, parking_time
    delete:
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
    update:
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
    list(login required):
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