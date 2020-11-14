from django.db import models


class Parking(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='parkings')
    lot = models.ForeignKey('lots.Lot', on_delete=models.CASCADE, related_name='parkings')
    start_time = models.DateTimeField(auto_now_add=True)
    parking_time = models.FloatField()
