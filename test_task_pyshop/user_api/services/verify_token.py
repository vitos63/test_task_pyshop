import jwt
from django.contrib.auth import get_user_model
from django.conf import settings

SECRET_KEY= settings.SECRET_KEY
User = get_user_model()


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['user_id'])
    
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return
