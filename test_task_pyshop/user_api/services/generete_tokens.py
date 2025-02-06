from datetime import timedelta
import uuid
from constance import config
import jwt
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from user_api.models import RefreshToken

SECRET_KEY= settings.SECRET_KEY
User = get_user_model()


def generate_access_token(user):
    access_exp = now() + timedelta(seconds=config.ACCESS_TOKEN_LIFETIME)
    access_token = jwt.encode(
        {
        'user_id':user.id, 
        'exp':access_exp,
        "iat": now(), 
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return access_token


def generate_refresh_token(user):
    refresh_token = uuid.uuid4()
    refresh_exp = now() + timedelta(seconds=config.REFRESH_TOKEN_LIFETIME)
    refresh_token,created = RefreshToken.objects.update_or_create(user = user, 
                                                                  defaults={
                                                                      'token':refresh_token, 
                                                                      'expires_at':refresh_exp
                                                                    }
                                                                )

    return str(refresh_token.token)




