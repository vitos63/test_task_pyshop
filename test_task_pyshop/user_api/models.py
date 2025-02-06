from datetime import timedelta
import uuid
from constance import config
from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class RefreshToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=now() + timedelta(seconds=config.REFRESH_TOKEN_LIFETIME))

    def __str__(self):
        return f'Refresh token for {self.user.username}'

