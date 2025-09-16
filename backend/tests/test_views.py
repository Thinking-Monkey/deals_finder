from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from unittest.mock import patch
from app.models import Store, Deal


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('signon')
        self.User = get_user_model()
        
    def test_register_first_user_becomes_admin(self):
        data = {
            'username': 'admin',
            'password': 'adminpass123',
            'passwordCheck': 'adminpass123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        user = self.User.objects.get(username='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_register_second_user_is_regular(self):
        # Create first user
        self.User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        data = {
            'username': 'regularuser',
            'password': 'userpass123',
            'passwordCheck': 'userpass123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = self.User.objects.get(username='regularuser')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        
    def test_register_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'passwordCheck': 'differentpass'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('signin')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_login_valid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('signout')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.refresh = RefreshToken.for_user(self.user)
        
    def test_logout_valid_token(self):
        data = {'refresh': str(self.refresh)}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
    def test_logout_invalid_token(self):
        data = {'refresh': 'invalid_token'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DealsListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('deals_list')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create stores
        self.store1 = Store.objects.create(store_id=1, store_name='Steam')
        self.store2 = Store.objects.create(store_id=7, store_name='GOG')
        self.store3 = Store.objects.create(store_id=11, store_name='Humble')
        
        # Create deals
        self.deal1 = Deal.objects.create(
            deal_id='DEAL1',
            title='Game 1',
            store=self.store1,
            store_name='Steam',
            sale_price=Decimal('19.99'),
            normal_price=Decimal('29.99'),
            deal_rating=Decimal('8.5')
        )
        self.deal2 = Deal.objects.create(
            deal_id='DEAL2',
            title='Game 2',
            store=self.store2,
            store_name='GOG',
            sale_price=Decimal('9.99'),
            normal_price=Decimal('19.99'),
            deal_rating=Decimal('9.0')
        )
        
    def test_deals_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['authenticated'])
        self.assertIn('deals', response.data)
        self.assertIn('count', response.data)
        
    def test_deals_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['authenticated'])
        self.assertIn('deals', response.data)
        self.assertIn('count', response.data)
        self.assertIn('page', response.data)
        self.assertIn('hasNext', response.data)
        
    def test_deals_list_pagination(self):
        # Create more deals to test pagination
        for i in range(10):
            Deal.objects.create(
                deal_id=f'DEAL{i+10}',
                title=f'Game {i+10}',
                store=self.store1,
                store_name='Steam',
                sale_price=Decimal('9.99'),
                normal_price=Decimal('19.99')
            )
            
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['page'], 2)


class DealDetailViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('deal_detail')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.store = Store.objects.create(store_id=1, store_name='Steam')
        self.deal = Deal.objects.create(
            deal_id='DEAL123',
            title='Test Game',
            store=self.store,
            store_name='Steam',
            sale_price=Decimal('19.99'),
            normal_price=Decimal('29.99'),
            deal_rating=Decimal('8.5')
        )
        
    def test_deal_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'deal_id': 'DEAL123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('deal', response.data)
        self.assertEqual(response.data['deal']['deal_id'], 'DEAL123')
        
    def test_deal_detail_unauthenticated(self):
        response = self.client.get(self.url, {'deal_id': 'DEAL123'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_deal_detail_missing_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_deal_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'deal_id': 'NONEXISTENT'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminExistViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('admin_exist')
        self.User = get_user_model()
        
    def test_admin_exist_no_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['adminExist'])
        
    def test_admin_exist_with_users(self):
        self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['adminExist'])