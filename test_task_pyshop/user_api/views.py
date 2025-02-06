from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user_api.services.generete_tokens import generate_access_token, generate_refresh_token
from user_api.services.refresh_tokens import refresh_tokens
from user_api.serializers import RegisterSerializer, ProfileSerializer
from user_api.models import RefreshToken

User = get_user_model()


class RegisterAPIView(APIView):
    authentication_classes = []
    
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    'id':user.id,
                    'username':user.username,
                    'email':user.email
                },
            status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        user_email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=user_email).first()
            
        if user:
            user = authenticate(username=user.username, password=password)

        if user:
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            return Response(
                {
                'access_token':access_token,
                'refresh_token':refresh_token
                }
            )
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        return refresh_tokens(refresh_token)


class LogoutApiView(APIView):
    authentication_classes = []

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken.objects.filter(token = refresh_token).first()
        
        if not token:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
        token.delete()

        return Response({'success': 'User logged out.'})


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
    
