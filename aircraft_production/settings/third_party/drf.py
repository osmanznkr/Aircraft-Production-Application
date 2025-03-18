from environs import Env

env = Env()
env.read_env(
    override=True  # For read environment variables firstly from .env file
)

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication', # For OAuth2
        'rest_framework.authentication.BasicAuthentication', # For Basic authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Default permission class
    ),

    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",  # for drf_standardized_errors
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",  # for drf_standardized_errors

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination', # Default pagination class
    'PAGE_SIZE': 100,

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter', # Default search filter
        'rest_framework.filters.OrderingFilter', # Default ordering filter
        'django_filters.rest_framework.DjangoFilterBackend' # Default Django filter backend
    ]
}
