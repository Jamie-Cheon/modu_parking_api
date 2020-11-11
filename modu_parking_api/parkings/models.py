from django.db import models


class Parking(models.Model):
    # FK 연결은 Class가 아니라 str으로 사용해서 순환참조 방지: https: // code.djangoproject.com / ticket / 167
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='parkings')
    lot = models.ForeignKey('lots.Lot', on_delete=models.CASCADE, related_name='parkings')
    start_time = models.DateTimeField(auto_now_add=True)
    parking_time = models.DurationField()

