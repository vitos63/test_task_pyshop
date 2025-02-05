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
        try:

            user_email = request.data.get('email')
            password = request.data.get('password')
            username = User.objects.get(email=user_email).username

            user = authenticate(username=username, password=password)

            if user:
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)

                return Response(
                    {
                    'access_token':access_token,
                    'refresh_token':refresh_token
                    }
                )
            
        except User.DoesNotExist:
            return Response({"error": "Wrong Email"}, status=status.HTTP_400_BAD_REQUEST)
        
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
        RefreshToken.objects.filter(token = refresh_token).delete()
        return Response({'success': 'User logged out.'})


class ProfileAPIView(RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
    
