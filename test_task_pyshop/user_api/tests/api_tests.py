from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from rest_framework.test import APIClient
from rest_framework import status
from user_api.services.generete_tokens import generate_access_token, generate_refresh_token
from user_api.models import RefreshToken

User = get_user_model()


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        user = authenticate(username = self.user.username, password = 'password123')
        self.access_token = generate_access_token(user)
        self.refresh_token = generate_refresh_token(user)
    

    def test_register_api_view(self):
        url = reverse('register')
        data = {
            'username': 'test_user1',
            'email':'test_user1@mail.ru',
            'password1':'password123',
            'password2':'password123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['email'],'test_user1@mail.ru')
        self.assertEqual(response.data['username'],'test_user1')
    

    def test_register_wrong_username(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email':'test_user1@mail.ru',
            'password1':'password123',
            'password2':'password123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    
    def test_register_wrong_email(self):
        url = reverse('register')
        data = {
            'username': 'test_user1',
            'email':'testuser@example.com',
            'password1':'password123',
            'password2':'password123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    

    def test_register_password1_not_equal_password2(self):
        url = reverse('register')
        data = {
            'username': 'test_user1',
            'email':'test_user1@mail.ru',
            'password1':'password123',
            'password2':'password'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)
    
    
    def test_login_api_view(self):
        url = reverse('login')
        data={
            'email':'testuser@example.com',
            'password':'password123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertTrue(User.objects.get(email=data['email']).is_authenticated)
    

    def test_login_wrong_email(self):
        url = reverse('login')
        data={
            'email':'test@example.com',
            'password':'password123'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"error": "Invalid credentials"}, response.data)
    

    def test_login_wrong_password(self):
        url = reverse('login')
        data={
            'email':'testuser@example.com',
            'password':'password'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"error": "Invalid credentials"}, response.data)
    
    
    def test_refresh_api_view(self):
        url = reverse('refresh')
        data = {
            'refresh_token':self.refresh_token
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh_token', response.data)
        self.assertIn('access_token', response.data)
        self.assertEqual(response.data['refresh_token'], str(User.objects.get(username='testuser').refreshtoken.token))
    

    def test_wrong_refresh_token(self):
        url = reverse('refresh')
        data = {
            'refresh_token':self.refresh_token
        }
        response_success = self.client.post(url, data)
        response_wrong = self.client.post(url, data)

        self.assertEqual(response_wrong.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_wrong.data, {'error':'Token not found'})
    

    def test_logout_api_view(self):   
        url = reverse('logout')
        data ={
            'refresh_token':self.refresh_token
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,{'success': 'User logged out.'})
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertFalse(RefreshToken.objects.filter(user=self.user.id).exists())
    

    def test_profile_api_view_get(self):
        url = reverse('me')
        response_data = {
            'id': User.objects.get(username='testuser').id,
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': '',
            'last_name': '',
        }
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)
    

    def test_profile_change_username(self):
        url = reverse('me')
        data = {
            'username':'new_test_user'
            }
        response_data = {
            'id': User.objects.get(username='testuser').id,
            'username': 'new_test_user',
            'email': 'testuser@example.com',
            'first_name': '',
            'last_name': '',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)
    

    def test_profile_change_email(self):
        url = reverse('me')
        data = {
            'email':'new_testuser@example.com'
            }
        response_data = {
            'id': User.objects.get(username='testuser').id,
            'username': 'testuser',
            'email': 'new_testuser@example.com',
            'first_name': '',
            'last_name': '',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)


    def test_profile_change_first_name(self):
        url = reverse('me')
        data = {
            'first_name':'first_name'
            }
        response_data = {
            'id': User.objects.get(username='testuser').id,
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'first_name',
            'last_name': '',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)
    

    def test_profile_change_last_name(self):
        url = reverse('me')
        data = {
            'last_name':'last_name'
            }
        response_data = {
            'id': User.objects.get(username='testuser').id,
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': '',
            'last_name': 'last_name',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)
    

    def test_wrong_token_profile(self):
        url = reverse('me')
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3Mzg3NzEzMTYsImlhdCI6MTczODc3MTI4Nn0.pEgtgy3Ocr-1LBo915wFzFIg_ZNoqbHAyoyk9HBklEsF')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    










        


    
