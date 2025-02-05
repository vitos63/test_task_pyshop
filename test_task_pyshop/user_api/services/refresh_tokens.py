from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework import status
from user_api.models import RefreshToken
from user_api.services.generete_tokens import generate_access_token, generate_refresh_token

def refresh_tokens(refresh_token):
    token_obj = RefreshToken.objects.filter(token = refresh_token).first()
    
    if not token_obj:
        return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if token_obj.expires_at < now():
        return Response({'error': 'Refresh token expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = token_obj.user
    token_obj.delete()

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return Response(
        {
        'access_token': access_token,
        'refresh_token': refresh_token
        }
    )


