from datetime import timedelta
from time import sleep
import jwt
from uuid import uuid4
from constance import config
from django.utils.timezone import now
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import RefreshToken
from user_api.services.generete_tokens import generate_access_token, generate_refresh_token
from user_api.services.refresh_tokens import refresh_tokens
from user_api.services.verify_token import verify_token


User = get_user_model()

class GenerateAccessTokenTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.secret_key = settings.SECRET_KEY


    def test_generate_access_token_returns_valid_token(self):
        token = generate_access_token(self.user)

        self.assertIsInstance(token, str)


    def test_access_token_contains_correct_payload(self):
        token = generate_access_token(self.user)
        decoded_token = jwt.decode(token, self.secret_key, algorithms=['HS256'])

        self.assertEqual(decoded_token['user_id'], self.user.id)
        self.assertIn('exp', decoded_token)
        self.assertIn('iat', decoded_token)


    def test_access_token_expiry_is_greater_than_iat(self):
        token = generate_access_token(self.user)
        decoded_token = jwt.decode(token, self.secret_key, algorithms=['HS256'])

        self.assertGreater(decoded_token['exp'], decoded_token['iat'])


    def test_access_tokens_are_different_on_multiple_calls(self):
        token1 = generate_access_token(self.user)
        sleep(1)
        token2 = generate_access_token(self.user)

        self.assertNotEqual(token1, token2)
    
   
class GenerateRefreshTokenTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')


    def test_generate_refresh_token_creates_valid_token(self):
        token = generate_refresh_token(self.user)

        self.assertIsInstance(token, str)
        self.assertTrue(RefreshToken.objects.filter(user=self.user).exists())


    def test_refresh_token_stores_correct_data(self):
        token = generate_refresh_token(self.user)
        refresh_token_obj = RefreshToken.objects.get(user=self.user)

        self.assertEqual(str(refresh_token_obj.token), token)
        self.assertTrue(refresh_token_obj.expires_at > now())


    def test_refresh_token_updates_instead_of_creating_new(self):
        token1 = generate_refresh_token(self.user)
        token2 = generate_refresh_token(self.user)

        self.assertEqual(RefreshToken.objects.filter(user=self.user).count(), 1)
        self.assertNotEqual(token1, token2)


    def test_refresh_token_expiry_time_is_correct(self):
        token = generate_refresh_token(self.user)
        refresh_token_obj = RefreshToken.objects.get(user=self.user)

        expected_expiry = now() + timedelta(seconds=config.REFRESH_TOKEN_LIFETIME)
        time_difference = int(abs((refresh_token_obj.expires_at - expected_expiry).total_seconds()))

        self.assertEqual(time_difference, 0)


class RefreshTokensTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.refresh_token = generate_refresh_token(self.user)


    def test_refresh_token_success(self):
        old_token = self.refresh_token
        response = refresh_tokens(old_token)

        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertNotEqual(old_token, response.data['refresh_token'])
        self.assertFalse(RefreshToken.objects.filter(token=old_token).exists())


    def test_refresh_token_not_found(self):
        response = refresh_tokens(uuid4())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token not found')


    def test_refresh_token_expired(self):
        RefreshToken.objects.filter(user=self.user).delete()
        expired_token_obj = RefreshToken.objects.create(
            user=self.user,
            token=uuid4(),
            expires_at=now() - timedelta(days=1)
        )
        response = refresh_tokens(expired_token_obj.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Refresh token expired')


class VerifyTokenTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.valid_token = generate_access_token(self.user)


    def test_verify_valid_token(self):
        user = verify_token(self.valid_token)

        self.assertEqual(user, self.user)


    def test_verify_expired_token(self):
        expired_payload = {
            'user_id': self.user.id,
            'exp': now() - timedelta(seconds=10),
            'iat': now() - timedelta(hours=1),
        }
        expired_token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm='HS256')
        user = verify_token(expired_token)

        self.assertIsNone(user)


    def test_verify_invalid_token(self):
        invalid_token = self.valid_token[:-5] + 'abcde'
        user = verify_token(invalid_token)

        self.assertIsNone(user)


    def test_verify_token_with_nonexistent_user(self):
        non_existent_payload = {
            'user_id': 0,
            'exp': now() + timedelta(hours=1),
            'iat': now(),
        }
        non_existent_token = jwt.encode(non_existent_payload, settings.SECRET_KEY, algorithm='HS256')
        user = verify_token(non_existent_token)
        
        self.assertIsNone(user)