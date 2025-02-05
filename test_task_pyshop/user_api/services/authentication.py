from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user_api.services.verify_token import verify_token



class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                raise AuthenticationFailed('Authorization scheme must be Bearer')
            
            user = verify_token(token)

            if not user:
                raise AuthenticationFailed('Invalid token')
            
            return user,token
        
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header format')
        
        except Exception as e:
            raise AuthenticationFailed(str(e)) 
    
