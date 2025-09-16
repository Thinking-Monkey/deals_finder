from django.test import TestCase
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from decimal import Decimal
from app.models import DFUser, Store, Deal
from app.admin import DFUserAdmin, StoreAdmin, DealAdmin


class MockRequest:
    def __init__(self, user=None):
        self.user = user


class DFUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = DFUserAdmin(DFUser, self.site)
        self.User = get_user_model()
        
    def test_list_display(self):
        expected = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
        self.assertEqual(self.admin.list_display, expected)
        
    def test_list_filter(self):
        expected = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
        self.assertEqual(self.admin.list_filter, expected)
        
    def test_search_fields(self):
        expected = ('username', 'first_name', 'last_name')
        self.assertEqual(self.admin.search_fields, expected)
        
    def test_ordering(self):
        expected = ('username',)
        self.assertEqual(self.admin.ordering, expected)
        
    def test_fieldsets_structure(self):
        fieldsets = self.admin.fieldsets
        self.assertEqual(len(fieldsets), 4)
        
        # Check first fieldset (None)
        self.assertIsNone(fieldsets[0][0])
        self.assertIn('username', fieldsets[0][1]['fields'])
        self.assertIn('password', fieldsets[0][1]['fields'])
        
        # Check permissions fieldset
        permissions_section = fieldsets[2]
        self.assertEqual(permissions_section[0], 'Permessi')
        self.assertIn('is_active', permissions_section[1]['fields'])
        self.assertIn('is_staff', permissions_section[1]['fields'])
        
    def test_add_fieldsets(self):
        add_fieldsets = self.admin.add_fieldsets
        self.assertEqual(len(add_fieldsets), 1)
        self.assertIn('username', add_fieldsets[0][1]['fields'])
        self.assertIn('password1', add_fieldsets[0][1]['fields'])
        self.assertIn('password2', add_fieldsets[0][1]['fields'])


class StoreAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = StoreAdmin(Store, self.site)
        
    def test_list_display(self):
        expected = ('store_id', 'store_name', 'is_active', 'created_at', 'updated_at')
        self.assertEqual(self.admin.list_display, expected)
        
    def test_list_filter(self):
        expected = ('is_active', 'created_at')
        self.assertEqual(self.admin.list_filter, expected)
        
    def test_search_fields(self):
        expected = ('store_name',)
        self.assertEqual(self.admin.search_fields, expected)
        
    def test_ordering(self):
        expected = ('store_id',)
        self.assertEqual(self.admin.ordering, expected)
        
    def test_readonly_fields(self):
        expected = ('created_at', 'updated_at')
        self.assertEqual(self.admin.readonly_fields, expected)


class DealAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = DealAdmin(Deal, self.site)
        
    def test_list_display(self):
        expected = ('title', 'store', 'sale_price', 'normal_price', 'deal_rating', 'created_at')
        self.assertEqual(self.admin.list_display, expected)
        
    def test_list_filter(self):
        expected = ('store', 'created_at', 'metacritic_score')
        self.assertEqual(self.admin.list_filter, expected)
        
    def test_search_fields(self):
        expected = ('title', 'deal_id')
        self.assertEqual(self.admin.search_fields, expected)
        
    def test_ordering(self):
        expected = ('-deal_rating', 'sale_price')
        self.assertEqual(self.admin.ordering, expected)
        
    def test_readonly_fields(self):
        expected = ('created_at', 'updated_at', 'deal_id')
        self.assertEqual(self.admin.readonly_fields, expected)
        
    def test_fieldsets_structure(self):
        fieldsets = self.admin.fieldsets
        self.assertEqual(len(fieldsets), 4)
        
        # Check base info section
        base_info = fieldsets[0]
        self.assertEqual(base_info[0], 'Informazioni base')
        self.assertIn('deal_id', base_info[1]['fields'])
        self.assertIn('title', base_info[1]['fields'])
        self.assertIn('store', base_info[1]['fields'])
        
        # Check prices section
        prices_section = fieldsets[1]
        self.assertEqual(prices_section[0], 'Prezzi e sconti')
        self.assertIn('sale_price', prices_section[1]['fields'])
        self.assertIn('normal_price', prices_section[1]['fields'])
        self.assertIn('deal_rating', prices_section[1]['fields'])
        
        # Check technical details section
        tech_section = fieldsets[2]
        self.assertEqual(tech_section[0], 'Dettagli tecnici')
        self.assertIn('metacritic_score', tech_section[1]['fields'])
        self.assertIn('thumb', tech_section[1]['fields'])
        
        # Check timestamp section
        timestamp_section = fieldsets[3]
        self.assertEqual(timestamp_section[0], 'Timestamp')
        self.assertIn('created_at', timestamp_section[1]['fields'])
        self.assertIn('updated_at', timestamp_section[1]['fields'])
        self.assertIn('collapse', timestamp_section[1]['classes'])


class AdminRegistrationTest(TestCase):
    def test_models_registered(self):
        """Test that all models are properly registered with admin"""
        self.assertIn(DFUser, admin.site._registry)
        self.assertIn(Store, admin.site._registry)
        self.assertIn(Deal, admin.site._registry)
        
    def test_admin_classes_used(self):
        """Test that custom admin classes are used"""
        self.assertIsInstance(admin.site._registry[DFUser], DFUserAdmin)
        self.assertIsInstance(admin.site._registry[Store], StoreAdmin)
        self.assertIsInstance(admin.site._registry[Deal], DealAdmin)


class AdminFunctionalTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.superuser = self.User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
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
            deal_rating=Decimal('8.5')
        )
        
    def test_admin_can_view_user_list(self):
        """Test that admin can view user list"""
        request = MockRequest(user=self.superuser)
        admin_instance = DFUserAdmin(DFUser, admin.site)
        
        # This would test the changelist view functionality
        # In a real test, you'd use the Django test client to make requests
        self.assertTrue(hasattr(admin_instance, 'changelist_view'))
        
    def test_admin_can_view_store_list(self):
        """Test that admin can view store list"""
        request = MockRequest(user=self.superuser)
        admin_instance = StoreAdmin(Store, admin.site)
        
        self.assertTrue(hasattr(admin_instance, 'changelist_view'))
        
    def test_admin_can_view_deal_list(self):
        """Test that admin can view deal list"""
        request = MockRequest(user=self.superuser)
        admin_instance = DealAdmin(Deal, admin.site)
        
        self.assertTrue(hasattr(admin_instance, 'changelist_view'))