from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('providers', views.ProviderView)
router.register('serviceAreas', views.ServiceAreaView)

urlpatterns = [
    path('', include(router.urls)),
]