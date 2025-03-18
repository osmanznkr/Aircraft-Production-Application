from django.urls import path
from rest_framework import routers

from accounts import views_api

router = routers.DefaultRouter(trailing_slash = False)
router.register('users', views_api.UserViewSet)

urlpatterns = [
    path('my-profile', views_api.UserRetrieveView.as_view(), name = "my_profile"),
    path('teams', views_api.TeamListView.as_view(), name = "teams"),
    path('team-types', views_api.TeamTypeListAPIView.as_view(), name = "team_types")
]

urlpatterns += router.urls