from environs import Env

env = Env()
env.read_env(
    override=True  # For read environment variables firstly from .env file
)

# OAuth2 settings
OAUTH2_PROVIDER = {
    'RESOURCE_SERVER_INTROSPECTION_URL': env.str('RESOURCE_SERVER_INTROSPECTION_URL'),
    'RESOURCE_SERVER_INTROSPECTION_CREDENTIALS': (env.str('CLIENT_ID'),
                                                  env.str('CLIENT_SECRET')),

    # required to avoid getting unsupported grant type error
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
}
