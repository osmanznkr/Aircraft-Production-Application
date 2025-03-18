"""
URL configuration for aircraft_production project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from drf_spectacular import views as spectacular_views

from aircraft_production import views
from aircraft_production.views import login_view

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
]

app_urls = i18n_patterns(
    path(
        "aircraft-admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "aircraft-admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path('aircraft-admin/', admin.site.urls),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    path('docs/default/',
         spectacular_views.SpectacularAPIView.as_view(),
         name='schema'),
    path('docs/redoc/', spectacular_views.SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    path('docs/', spectacular_views.SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),

    # Other apps
    path('accounts/', include('accounts.urls_api')),
    path('permissions/', include('permissions.urls_api')),
    path('aircrafts/', include('aircrafts.urls_api')),
    path('inventories/', views.inventories, name='inventories'),
    path('stocks/', views.stocks, name='stocks'),
    path('managers/', views.managers, name='managers'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
)

urlpatterns += app_urls

# This condition is development and production control for static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
