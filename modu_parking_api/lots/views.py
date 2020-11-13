from rest_framework import viewsets
from rest_framework.decorators import action
from lots.models import Lot
from lots.serializers import LotsSerializer, MapSerializer


class LotsViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer

    def get_serializer_class(self):
        if self.action == 'map':
            return MapSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        data = self.request.GET     # User's location
        if self.action == 'map':
            lat = float(data['latitude'])
            lon = float(data['longitude'])

            min_lat = lat - 0.009
            max_lat = lat + 0.009
            min_lon = lon - 0.015
            max_lon = lon + 0.015

            # filter by setting the minimum and maximum latitude and longitude by 1km
            queryset = self.queryset.filter(latitude__gte=min_lat, latitude__lte=max_lat,
                                            longitude_gte=min_lon, longitude__lte=max_lon)
            return queryset
        return super().get_queryset()

    @action(detail=False)
    def map(self, request, *args, **kwargs):
        """
        A list of parking lots in a range based on the user's location
        """
        return super().list(request, *args, **kwargs)
