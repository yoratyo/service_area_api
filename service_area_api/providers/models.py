from django.db import models
from django.contrib.gis.db.models import PolygonField


class Provider(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_summarized(self):
        return '{} ({}) - {}'.format(self.name, self.email, self.currency)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    polygon = PolygonField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_summarized(self):
        return '{} ({}) - {}'.format(self.name, self.provider.name, self.price)

    def __str__(self):
        return self.name
