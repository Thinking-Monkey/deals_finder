from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from decimal import Decimal
from app.models import Store, Deal
from app.serializers import (
    DFUserSerializer, LoginSerializer, StoreSerializer,
    DealSerializer, DealPublicSerializer
)


class DFUserSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        
    def test_valid_user_serializer(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'passwordCheck': 'testpass123'
        }
        serializer = DFUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'passwordCheck': 'differentpass'
        }
        serializer = DFUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Passwords does not match.', str(serializer.errors))
        
    def test_create_regular_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'passwordCheck': 'testpass123'
        }
        serializer = DFUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        
    def test_create_superuser(self):
        data = {
            'username': 'admin',
            'password': 'adminpass123',
            'passwordCheck': 'adminpass123',
            'is_superuser': True
        }
        serializer = DFUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save(is_superuser=True)
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class LoginSerializerTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_valid_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
        
    def test_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Credentials are not valid.', str(serializer.errors))
                
    def test_missing_fields(self):
        data = {'username': 'testuser'}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        error = serializer.errors
        self.assertIn('This field is required.', str(error))


class StoreSerializerTest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        
    def test_store_serialization(self):
        serializer = StoreSerializer(self.store)
        data = serializer.data
        self.assertEqual(data['store_id'], 1)
        self.assertEqual(data['store_name'], 'Steam')
        self.assertTrue(data['is_active'])
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        
    def test_store_deserialization(self):
        data = {
            'store_id': 2,
            'store_name': 'GOG',
            'is_active': True
        }
        serializer = StoreSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        store = serializer.save()
        self.assertEqual(store.store_id, 2)
        self.assertEqual(store.store_name, 'GOG')


class DealSerializerTest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        self.deal = Deal.objects.create(
            deal_id='DEAL123',
            title='Test Game',
            store=self.store,
            store_name='Steam',
            sale_price=Decimal('19.99'),
            normal_price=Decimal('29.99'),
            deal_rating=Decimal('8.5'),
            thumb='https://example.com/thumb.jpg'
        )
        
    def test_deal_serialization(self):
        serializer = DealSerializer(self.deal)
        data = serializer.data
        self.assertEqual(data['deal_id'], 'DEAL123')
        self.assertEqual(data['title'], 'Test Game')
        self.assertEqual(data['store_name'], 'Steam')
        self.assertEqual(data['sale_price'], '19.99')
        self.assertEqual(data['normal_price'], '29.99')
        self.assertEqual(data['deal_rating'], '8.5')
        
    def test_deal_public_serialization(self):
        serializer = DealPublicSerializer(self.deal)
        data = serializer.data
        expected_fields = {
            'deal_id', 'title', 'store_name', 'sale_price', 
            'normal_price', 'thumb'
        }
        self.assertEqual(set(data.keys()), expected_fields)
        self.assertEqual(data['deal_id'], 'DEAL123')
        self.assertEqual(data['title'], 'Test Game')
        self.assertEqual(data['store_name'], 'Steam')