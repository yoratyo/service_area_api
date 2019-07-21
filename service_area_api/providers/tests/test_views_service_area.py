from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import ServiceArea, Provider
from ..serializers import ServiceAreaSerializer
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.contrib.gis.geos import Polygon


# initialize the APIClient app
client = Client()

factory = APIRequestFactory()
request = factory.get('/')

serializer_context = {
    'request': Request(request),
}

class ServiceAreaTest(TestCase):
    """ Test module for GET all providers API """

    def setUp(self):
        self.provider = Provider.objects.create(
            name='TransJakarta',
            email='tj@gmail.com',
            phone_number='+622134352',
            language='English',
            currency='IDR',
        )

        self.bandung = ServiceArea.objects.create(
            name='Bandung',
            price=70000.0,
            provider=self.provider,
            polygon=Polygon( (
                (107.60456085205078, -6.883652362379861),
                (107.55392074584961, -6.932391109013438),
                (107.63322830200195, -6.9613593064322625),
                (107.60456085205078, -6.883652362379861)) ),
        )
        self.garut = ServiceArea.objects.create(
            name='Garut',
            price=50000.0,
            provider=self.provider,
            polygon=Polygon((
                (107.60456085205078, -6.883652362379861),
                (107.55392074584961, -6.932391109013438),
                (107.63322830200195, -6.9613593064322625),
                (107.60456085205078, -6.883652362379861))),
        )

    def test_get_all_service_area(self):
        # get API response
        response = client.get(reverse('servicearea-list'))
        # get data from db
        area = ServiceArea.objects.all()
        serializer = ServiceAreaSerializer(area, many=True, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_service_area(self):
        response = client.get(
            reverse('servicearea-detail', kwargs={'pk':self.bandung.id}))
        area = ServiceArea.objects.get(id=self.bandung.id)
        serializer = ServiceAreaSerializer(area, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_service_area(self):
        response = client.get(
            reverse('servicearea-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_delete_service_area(self):
        response = client.delete(
            reverse('servicearea-detail', kwargs={'pk':self.bandung.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_provider(self):
        response = client.delete(
            reverse('servicearea-detail', kwargs={'pk':20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_search_service_area(self):
        # get API response
        response = client.get(
            reverse('servicearea-search'),
            {'longitude': 107.60490417480469, 'latitude': -6.960507326113321}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_search_service_area(self):
        # get API response
        response = client.get(
            reverse('servicearea-search')
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)