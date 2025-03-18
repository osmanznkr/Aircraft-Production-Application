from django.urls import path
from rest_framework import routers

from aircrafts import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('inventories/stocks', views.InventoryCountViewSet, basename='stocks')
router.register('inventories', views.InventoryViewSet, basename='inventories')
router.register('', views.AircraftViewSet, basename='aircrafts')

urlpatterns = [
    path('inventories/inventory-types', views.InventoryTypeListAPIView.as_view(), name='inventory_types'),
    path('aircraft-types', views.AircraftTypeListAPIView.as_view(), name='aircraft_types'),
]

urlpatterns += router.urls