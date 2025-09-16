from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from decimal import Decimal
from app.models import Store, Deal
from app.admin import DFUserAdmin, StoreAdmin, DealAdmin


class MockRequest:
    pass


class DFUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.User = get_user_model()
        self.admin = DFUserAdmin(self.User, self.site)
        
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
        
    def test_fieldsets(self):
        self.assertEqual(len(self.admin.fieldsets), 4)
        # Check first fieldset (None section)
        self.assertEqual(self.admin.fieldsets[0][1]['fields'], ('username', 'password'))
        # Check personal info section
        self.assertEqual(self.admin.fieldsets[1][0], 'Informazioni personali')
        
    def test_add_fieldsets(self):
        self.assertEqual(len(self.admin.add_fieldsets), 1)
        self.assertEqual(self.admin.add_fieldsets[0][1]['fields'], ('username', 'password1', 'password2'))


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
        
    def test_fieldsets(self):
        self.assertEqual(len(self.admin.fieldsets), 4)
        # Check fieldset names
        fieldset_names = [fs[0] for fs in self.admin.fieldsets]
        expected_names = ['Informazioni base', 'Prezzi e sconti', 'Dettagli tecnici', 'Timestamp']
        self.assertEqual(fieldset_names, expected_names)
        
        # Check that timestamp fieldset is collapsible
        timestamp_fieldset = self.admin.fieldsets[3]
        self.assertIn('collapse', timestamp_fieldset[1]['classes'])


class AdminIntegrationTest(TestCase):
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
        
    def test_admin_site_registration(self):
        from django.contrib import admin
        
        # Check that models are registered
        self.assertIn(self.User, admin.site._registry)
        self.assertIn(Store, admin.site._registry)
        self.assertIn(Deal, admin.site._registry)
        
        # Check that correct admin classes are used
        self.assertIsInstance(admin.site._registry[self.User], DFUserAdmin)
        self.assertIsInstance(admin.site._registry[Store], StoreAdmin)
        self.assertIsInstance(admin.site._registry[Deal], DealAdmin)
        
    def test_admin_login_required(self):
        response = self.client.get('/admin/')
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        
    def test_admin_access_with_superuser(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        
    def test_store_admin_changelist(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/app/store/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Steam')
        
    def test_deal_admin_changelist(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/app/deal/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')
        
    def test_user_admin_changelist(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/app/dfuser/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')