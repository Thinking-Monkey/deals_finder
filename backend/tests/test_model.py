from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from app.models import DFUser, Store, Deal


class DFUserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_str_representation(self):
        user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                username='',
                password='testpass123'
            )

    def test_create_superuser_without_username(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username='',
                password='adminpass123'
            )

    def test_user_full_name(self):
        user = self.User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')


class StoreModelTest(TestCase):
    def setUp(self):
        self.store_data = {
            'store_id': 1,
            'store_name': 'Steam',
            'is_active': True
        }

    def test_create_store(self):
        store = Store.objects.create(**self.store_data)
        self.assertEqual(store.store_id, 1)
        self.assertEqual(store.store_name, 'Steam')
        self.assertTrue(store.is_active)
        self.assertIsNotNone(store.created_at)
        self.assertIsNotNone(store.updated_at)

    def test_store_str_representation(self):
        store = Store.objects.create(**self.store_data)
        expected_str = f"{store.store_name} ({store.store_id})"
        self.assertEqual(str(store), expected_str)

    def test_store_default_active(self):
        store = Store.objects.create(
            store_id=2,
            store_name='GOG'
        )
        self.assertTrue(store.is_active)

    def test_store_unique_id(self):
        Store.objects.create(**self.store_data)
        with self.assertRaises(Exception):
            Store.objects.create(**self.store_data)


class DealModelTest(TestCase):
    def setUp(self):
        self.store = Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        self.deal_data = {
            'deal_id': 'DEAL123',
            'title': 'Test Game',
            'store': self.store,
            'store_name': 'Steam',
            'sale_price': Decimal('19.99'),
            'normal_price': Decimal('29.99'),
            'deal_rating': Decimal('8.5'),
            'thumb': 'https://example.com/thumb.jpg'
        }

    def test_create_deal(self):
        deal = Deal.objects.create(**self.deal_data)
        self.assertEqual(deal.deal_id, 'DEAL123')
        self.assertEqual(deal.title, 'Test Game')
        self.assertEqual(deal.store, self.store)
        self.assertEqual(deal.store_name, 'Steam')
        self.assertEqual(deal.sale_price, Decimal('19.99'))
        self.assertEqual(deal.normal_price, Decimal('29.99'))
        self.assertEqual(deal.deal_rating, Decimal('8.5'))
        self.assertIsNotNone(deal.created_at)
        self.assertIsNotNone(deal.updated_at)

    def test_deal_str_representation(self):
        deal = Deal.objects.create(**self.deal_data)
        expected_str = f"{deal.title} - ${deal.sale_price}"
        self.assertEqual(str(deal), expected_str)

    def test_deal_optional_fields(self):
        deal = Deal.objects.create(
            deal_id='DEAL124',
            title='Another Game',
            store=self.store,
            store_name='Steam',
            sale_price=Decimal('9.99'),
            normal_price=Decimal('19.99'),
            metacritic_score=85,
            release_date=timezone.now(),
            last_change=timezone.now()
        )
        self.assertEqual(deal.metacritic_score, 85)
        self.assertIsNotNone(deal.release_date)
        self.assertIsNotNone(deal.last_change)

    def test_deal_ordering(self):
        deal1 = Deal.objects.create(
            deal_id='DEAL1',
            title='Game 1',
            store=self.store,
            store_name='Steam',
            sale_price=Decimal('20.00'),
            normal_price=Decimal('30.00'),
            deal_rating=Decimal('7.0')
        )
        deal2 = Deal.objects.create(
            deal_id='DEAL2',
            title='Game 2',
            store=self.store,
            store_name='Steam',
            sale_price=Decimal('10.00'),
            normal_price=Decimal('30.00'),
            deal_rating=Decimal('9.0')
        )
        deals = Deal.objects.all()
        self.assertEqual(deals[0], deal2)  # Higher rating first
        self.assertEqual(deals[1], deal1)

    def test_deal_foreign_key_cascade(self):
        deal = Deal.objects.create(**self.deal_data)
        self.assertEqual(Deal.objects.count(), 1)
        self.store.delete()
        self.assertEqual(Deal.objects.count(), 0)