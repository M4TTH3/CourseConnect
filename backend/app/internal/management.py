"""
Interact with AUTH0 Management API
"""

import requests as req
from .settings import get_settings
from typing import Tuple, Annotated

def get_access_token() -> Tuple[Annotated[str, 'access_token'], Annotated[str, 'audience']]:
    config = get_settings()
    payload: dict = req.post(config.management_token_endpoint, data={
        'client_id': config.management_client_id,
        'client_secret': config.management_client_secret,
        'audience': config.management_aud,
        'grant_type': 'client_credentials' 
    }).json()
    
    access_token = payload.get('access_token')
    
    return access_token, config.management_aud
