from django.urls import path

from permissions import views_api

urlpatterns = [
    path('my', views_api.MyPermissionListView.as_view(), name='my-permissions'),
]