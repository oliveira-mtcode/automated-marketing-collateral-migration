from typing import Optional
from boxsdk import JWTAuth, Client
from app.config.settings import settings


def get_box_client() -> Client:
    if settings.box_jwt_private_key:
        auth = JWTAuth(
            client_id=settings.box_client_id,
            client_secret=settings.box_client_secret,
            enterprise_id=settings.box_enterprise_id,
            jwt_key_id=settings.box_jwt_private_key_id,
            rsa_private_key_data=settings.box_jwt_private_key,
            rsa_private_key_passphrase=settings.box_jwt_passphrase.encode() if settings.box_jwt_passphrase else None,
        )
        access_token = auth.authenticate_instance()
        return Client(auth)
    raise RuntimeError("Only JWT authentication is implemented for Box in this template.")


