from django.test import TestCase
from ..models import Provider, ServiceArea
from django.contrib.gis.geos import Polygon


class ProviderTest(TestCase):
    """ Test module for Provider model """

    def setUp(self):
        Provider.objects.create(
            name='TransJakarta',
            email='tj@gmail.com',
            phone_number='+622134352',
            language='English',
            currency='IDR',
        )
        Provider.objects.create(
            name='Primajasa',
            email='primajasa@gmail.com',
            phone_number='+6224523',
            language='Indonesian',
            currency='IDR',
        )

    def test_get_provider(self):
        provider_1 = Provider.objects.get(name='TransJakarta')
        provider_2 = Provider.objects.get(name='Primajasa')
        self.assertEqual(
            provider_1.get_summarized(), "TransJakarta (tj@gmail.com) - IDR")
        self.assertEqual(
            provider_2.get_summarized(), "Primajasa (primajasa@gmail.com) - IDR")


class ServiceAreaTest(TestCase):
    """ Test module for ServiceArea model """

    def setUp(self):
        provider = Provider.objects.create(
            name='TransJakarta')

        ServiceArea.objects.create(
            name='Jakarta',
            price=3500.0,
            provider=provider,
            polygon=Polygon( ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)) ),
        )

    def test_get_provider(self):
        area_1 = ServiceArea.objects.get(name='Jakarta')
        self.assertEqual(
            area_1.get_summarized(), "Jakarta (TransJakarta) - 3500.00")
