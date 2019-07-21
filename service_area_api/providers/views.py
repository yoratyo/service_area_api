from rest_framework import  viewsets
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ProviderView(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaView(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    # Cache requested url for each user for 1 hours
    @method_decorator(cache_page(60*60))
    @action(methods=['get'], detail=False)
    def search(self, request):
        # Search included service area by long/lat pair
        try:
            longitude = request.query_params.get('longitude')
            latitude = request.query_params.get('latitude')

            pnt = GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)
            result = ServiceArea.objects.filter(polygon__contains=pnt)
            serializer = self.get_serializer(result, many=True)

            return Response(serializer.data)
        except:
            return Response({"Error": "Make sure you set longitude & latitude correctly"})
