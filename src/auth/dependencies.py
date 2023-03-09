'''dependencies.py - Dependency Injection for router.py'''

import src.config as config
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App


class Auth0:
    AUTH0 = None
    
    @classmethod
    def client(cls) -> StarletteOAuth2App:
        if cls.AUTH0 == None:
            cls.register()
        return cls.AUTH0

    @classmethod
    def register(cls):
        oauth = OAuth()
        oauth.register(
            name='auth0',
            client_id=config.AUTH0_CLIENT_ID,
            client_secret=config.AUTH0_CLIENT_SECRET,
            api_base_url=config.AUTH0_DOMAIN,
            access_token_url=f'https://{config.AUTH0_DOMAIN}/oauth/token',
            authorize_url=f'https://{config.AUTH0_DOMAIN}/authorize',
            client_kwargs={
                'scope': 'openid profile email',
            },
            server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration',
        )
        cls.AUTH0 = oauth.auth0


