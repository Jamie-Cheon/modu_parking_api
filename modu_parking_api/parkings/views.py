from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from lots.models import Lot
from parkings.models import Parking
from parkings.permissions import IsOwner
from parkings.serializers import ParkingSerializer, ParkingListSerializer


class ParkingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = (IsOwner,)

    def get_serializer_class(self):
        if self.action == "list":
            return ParkingListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        POST /parkings/
        Deduct points when a user is making parking payment

        Total fee = Basic charge for the first hour of parking time, and additional charge for the remaining hours
        """
        lot = Lot.objects.get(id=request.data['lot'])
        # lot = get_object_or_404(Lot, pk=request.data['lot'])
        parking_time = float(request.data['parking_time'])
        additional_rate = ((parking_time - 1) * 2) * lot.additional_rate
        total_fee = (lot.basic_rate + additional_rate)

        if request.user.points < total_fee:
            return Response({'refuse': 'Not enough points'})

        # 포인트 차감/충전 동시에 진행 하면 race condition 발생 가능
        # 해결: lock/F function/Update
        # https://docs.djangoproject.com/en/3.0/ref/models/expressions/#f-expressions
        # https: // docs.djangoproject.com / en / 3.0 / ref / models / expressions /  # avoiding-race-conditions-using-f
        # User.objects.filter(id=request.user.id).update(points=F('points') - total_fee)

        # 사용자 포인트 차감
        request.user.points -= total_fee
        request.user.save()
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        GET /parkings/
        : user's parking history (parking time, total fee, lot details..)
        """
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # queryset도 dynamic 하게 override 가능
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if self.action == 'list':
    #         qs = qs.filter(user=self.request.user)
    #         return qs
    #     return qs

    def update(self, request, *args, **kwargs):
        """
        PUT /parkings/id/
        : Deduct additional fee when a user extend parking time
        """
        instance = self.get_object()
        additional_time = float(request.data['additional_time'])
        lot = Lot.objects.get(id=instance.lot_id)
        additional_rate = (additional_time * 2) * lot.additional_rate

        if request.user.points < additional_rate:
            return Response({'refuse': 'Not enough points'})

        instance.parking_time += additional_time
        request.user.points -= additional_rate

        request.user.save()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
