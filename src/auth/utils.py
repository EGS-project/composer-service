'''utils.py - non-business logic functions, e.g. response normalization, data enrichment, etc.'''


from urllib.parse import quote_plus, urlencode
from fastapi import Request, Response
from starlette.responses import RedirectResponse
import src.config as config
from jose import jwt


def set_session_cookie(response: Response, userdata: dict):
    response.set_cookie(key = config.APP_COOKIE_NAME,
                        value = encoded_value(userdata),
                        domain = config.APP_HOST,
                        path = '/',
                        samesite="none",
                        secure=True)

def expire_session_cookie(response: Response):
    response.delete_cookie( key = config.APP_COOKIE_NAME,
                            domain = config.APP_HOST,
                            path = '/',
                            samesite = "none",
                            secure=True)
    
def encoded_value(value):
    return jwt.encode(value, config.APP_SECRET_KEY)

def decoded_value(value):
    return jwt.decode(value, config.APP_SECRET_KEY)


def logout_auth0(redirect_uri: str):
    return RedirectResponse(
        url=f"https://{config.AUTH0_DOMAIN}/v2/logout?" 
        + urlencode(
            {
                "returnTo": redirect_uri,
                "client_id": config.AUTH0_CLIENT_ID
            },
            quote_via=quote_plus,
        )
    )
