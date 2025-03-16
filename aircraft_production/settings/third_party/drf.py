from environs import Env

env = Env()
env.read_env(
    override=True  # For read environment variables firstly from .env file
)

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",  # for drf_standardized_errors
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",  # for drf_standardized_errors

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}
