from random import *
from haversine import haversine
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from lots.models import Lot


class LotsTestCase(APITestCase):
    def setUp(self) -> None:
        self.lots = baker.make(Lot, _quantity=3)

    def test_create(self):
        data = {
            "name": 'Robson parking #1',
            "address": '120 robson st',
            "latitude": 127.77,
            "longitude": 352.123,
            "basic_rate": 10000,
            "additional_rate": 6000,
            "section_count": 1,
            "time_weekdays": '12:00 ~ 22:00',
            "time_weekends": '12:00 ~ 22:00',
        }
        response = self.client.post('/api/lots', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('name'))
        self.assertEqual(response.data.get('latitude'), data['latitude'])

    def test_retrieve(self):
        # 권한을 주지 않아서 아직 사용하지 않습니다. 하게 된다면 유저를 생성하고, 사용하시면 됩니다.
        response = self.client.get(f'/api/lots/{self.lots[0].pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.lots[0].name, response.data.get('name'))

    def test_update(self):
        data = {
            "name": 'Alberni st parking',
            "address": '456 alberni st',
            "latitude": '127.79',
            "longitude": '352.129',
            "basic_rate": '20000 ',
            "additional_rate": '2000 ',
            "section_count": '2'
        }
        response = self.client.patch(f'/api/lots/{self.lots[0].pk}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], response.data.get('name'))

    def test_delete(self):
        response = self.client.delete(f'/api/lots/{self.lots[0].id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lot.objects.filter(id=self.lots[0].id).count(), 0)


class LotsListTestCase(APITestCase):

    def setUp(self) -> None:

        lat_min = 37.537
        lat_max = 37.587
        lng_min = 126.951
        lng_max = 127.036

        rate_min = 10
        rate_max = 50

        # create lots with random location and basic_rate
        for i in range(500):
            rate = randint(rate_min, rate_max) * 1000  # return integer
            lat = uniform(lat_min, lat_max)  # return float
            lng = uniform(lng_min, lng_max)
            Lot.objects.create(address=f'{i} Robson st', latitude=lat, longitude=lng, name=f'{i}lot', basic_rate=rate,
                               additional_rate=rate // 2, time_weekdays='12:00 ~ 22:00', time_weekends='12:00 ~ 22:00',
                               section_count=i % 20, )

        # user coordinate
        self.lat = uniform(lat_min, lat_max)
        self.lng = uniform(lng_min, lng_max)

    def test_map_list(self):
        # data for request body
        # radius : In order to retrieve lots within 2km
        user_location = {'lat': self.lat, 'lon': self.lng, 'radius': 2}

        response = self.client.get('/api/lots/map', data=user_location)
        self.assertEqual(response.status_code, 200)

        for lot in response.data:
            lat = lot['latitude']
            lng = lot['longitude']
            lot_location = (lat, lng)

            # distance between user and lot should be within 2km
            # haversine : return distance between two locations
            distance = haversine(lot_location, (self.lat, self.lng))
            self.assertLessEqual(distance, user_location['radius'])


