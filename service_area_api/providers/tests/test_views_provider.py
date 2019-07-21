import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Provider
from ..serializers import ProviderSerializer
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


# initialize the APIClient app
client = Client()

factory = APIRequestFactory()
request = factory.get('/')

serializer_context = {
    'request': Request(request),
}

class ProviderTest(TestCase):
    """ Test module for GET all providers API """

    def setUp(self):
        self.transjakarta = Provider.objects.create(
            name='TransJakarta',
            email='tj@gmail.com',
            phone_number='+622134352',
            language='English',
            currency='IDR',
        )
        self.primajasa = Provider.objects.create(
            name='Primajasa',
            email='primajasa@gmail.com',
            phone_number='+6224523',
            language='Indonesian',
            currency='IDR',
        )

    def test_get_all_providers(self):
        # get API response
        response = client.get(reverse('provider-list'))
        # get data from db
        provider = Provider.objects.all()
        serializer = ProviderSerializer(provider, many=True, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_provider(self):
        response = client.get(
            reverse('provider-detail', kwargs={'pk':self.primajasa.id}))
        provider = Provider.objects.get(id=self.primajasa.id)
        serializer = ProviderSerializer(provider, context=serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_provider(self):
        response = client.get(
            reverse('provider-detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_provider(self):
        valid_payload = {
            'name':'TransJakarta',
            'email':'tj@gmail.com',
            'phone_number':'+622134352',
            'language':'English',
            'currency':'IDR',
        }

        response = client.post(
            reverse('provider-list'),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_provider(self):
        invalid_payload = {
            'name': '',
            'email': '',
            'phone_number': '+622134352',
            'language': 'English',
            'currency': 'IDR',
        }

        response = client.post(
            reverse('provider-list'),
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_provider(self):
        valid_payload = {
            'name': 'TransJakarta',
            'email': 'transjkt@gmail.com',
            'phone_number': '+622134352',
            'language': 'Javanese',
            'currency': 'IDR',
        }

        response = client.put(
            reverse('provider-detail', kwargs={'pk':self.primajasa.id}),
            data=json.dumps(valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_provider(self):
        invalid_payload = {
            'name': '',
            'email': '',
            'phone_number': '+622134352',
            'language': 'English',
            'currency': 'IDR',
        }

        response = client.put(
            reverse('provider-detail', kwargs={'pk':self.transjakarta.id}),
            data=json.dumps(invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_provider(self):
        response = client.delete(
            reverse('provider-detail', kwargs={'pk':self.transjakarta.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_provider(self):
        response = client.delete(
            reverse('provider-detail', kwargs={'pk':20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)