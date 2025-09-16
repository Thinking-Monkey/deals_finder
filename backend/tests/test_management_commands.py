from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, Mock, MagicMock
from io import StringIO
from decimal import Decimal
from app.models import Store, Deal


class FetchDealsCommandTest(TestCase):
    def setUp(self):
        self.mock_stores_response = [
            {
                'storeID': '1',
                'storeName': 'Steam',
                'isActive': 1
            },
            {
                'storeID': '7', 
                'storeName': 'GOG',
                'isActive': 1
            }
        ]
        
        self.mock_deals_response = [
            {
                'dealID': 'DEAL123',
                'title': 'Test Game',
                'storeID': '1',
                'salePrice': '19.99',
                'normalPrice': '29.99',
                'dealRating': '8.5',
                'thumb': 'https://example.com/thumb.jpg',
                'metacriticScore': '85',
                'releaseDate': '1640995200',  # 2022-01-01
                'lastChange': '1640995200'
            }
        ]

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_fetch_stores_success(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_stores_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Capture output
        out = StringIO()
        call_command('fetch_deals', '--stores-only', stdout=out)
        
        # Verify stores were created
        self.assertEqual(Store.objects.count(), 2)
        steam_store = Store.objects.get(store_id=1)
        self.assertEqual(steam_store.store_name, 'Steam')
        self.assertTrue(steam_store.is_active)
        
        # Verify output
        output = out.getvalue()
        self.assertIn('Created store: Steam', output)
        self.assertIn('Stores fetch completed', output)

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_fetch_deals_success(self, mock_get):
        # Create a store first
        store = Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_deals_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        out = StringIO()
        call_command('fetch_deals', '--deals-only', stdout=out)
        
        # Verify deal was created
        self.assertEqual(Deal.objects.count(), 1)
        deal = Deal.objects.get(deal_id='DEAL123')
        self.assertEqual(deal.title, 'Test Game')
        self.assertEqual(deal.store, store)
        self.assertEqual(deal.sale_price, Decimal('19.99'))
        self.assertEqual(deal.metacritic_score, 85)
        
        output = out.getvalue()
        self.assertIn('Created deal: Test Game', output)

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_fetch_both_stores_and_deals(self, mock_get):
        # Mock responses for both calls
        def side_effect(url):
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            if 'stores' in url:
                mock_response.json.return_value = self.mock_stores_response
            else:
                mock_response.json.return_value = self.mock_deals_response
            return mock_response
        
        mock_get.side_effect = side_effect
        
        out = StringIO()
        call_command('fetch_deals', stdout=out)
        
        # Verify both stores and deals were created
        self.assertEqual(Store.objects.count(), 2)
        self.assertEqual(Deal.objects.count(), 1)
        
        output = out.getvalue()
        self.assertIn('Created store: Steam', output)
        self.assertIn('Created deal: Test Game', output)

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_fetch_stores_network_error(self, mock_get):
        mock_get.side_effect = Exception('Network error')
        
        with self.assertRaises(CommandError):
            call_command('fetch_deals', '--stores-only')

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_fetch_deals_network_error(self, mock_get):
        mock_get.side_effect = Exception('Network error')
        
        with self.assertRaises(CommandError):
            call_command('fetch_deals', '--deals-only')

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_update_existing_store(self, mock_get):
        # Create existing store
        Store.objects.create(
            store_id=1,
            store_name='Old Name',
            is_active=False
        )
        
        mock_response = Mock()
        mock_response.json.return_value = self.mock_stores_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        out = StringIO()
        call_command('fetch_deals', '--stores-only', stdout=out)
        
        # Verify store was updated
        store = Store.objects.get(store_id=1)
        self.assertEqual(store.store_name, 'Steam')
        self.assertTrue(store.is_active)
        
        output = out.getvalue()
        self.assertIn('Updated store: Steam', output)

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_update_existing_deal(self, mock_get):
        # Create store and existing deal
        store = Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        
        Deal.objects.create(
            deal_id='DEAL123',
            title='Old Title',
            store=store,
            store_name='Steam',
            sale_price=Decimal('9.99'),
            normal_price=Decimal('19.99')
        )
        
        mock_response = Mock()
        mock_response.json.return_value = self.mock_deals_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        out = StringIO()
        call_command('fetch_deals', '--deals-only', stdout=out)
        
        # Verify deal was updated
        deal = Deal.objects.get(deal_id='DEAL123')
        self.assertEqual(deal.title, 'Test Game')
        self.assertEqual(deal.sale_price, Decimal('19.99'))
        
        output = out.getvalue()
        self.assertIn('Updated deal: Test Game', output)

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_deal_with_missing_optional_fields(self, mock_get):
        # Create store first
        Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        
        # Mock deal with missing optional fields
        deal_data = {
            'dealID': 'DEAL124',
            'title': 'Simple Game',
            'storeID': '1',
            'salePrice': '9.99',
            'normalPrice': '19.99',
            'dealRating': '7.0',
            'thumb': '',
            'metacriticScore': '',
            'releaseDate': '0',
            'lastChange': '0'
        }
        
        mock_response = Mock()
        mock_response.json.return_value = [deal_data]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        out = StringIO()
        call_command('fetch_deals', '--deals-only', stdout=out)
        
        # Verify deal was created with None values for optional fields
        deal = Deal.objects.get(deal_id='DEAL124')
        self.assertEqual(deal.title, 'Simple Game')
        self.assertIsNone(deal.metacritic_score)
        self.assertIsNone(deal.release_date)
        self.assertIsNone(deal.last_change)

    @patch('app.management.commands.fetch_deals.requests.get')
    def test_deal_with_invalid_data_continues_processing(self, mock_get):
        # Create store first
        Store.objects.create(
            store_id=1,
            store_name='Steam',
            is_active=True
        )
        
        # Mock response with one invalid and one valid deal
        invalid_deal = {
            'dealID': 'INVALID',
            # Missing required fields
        }
        
        valid_deal = self.mock_deals_response[0].copy()
        valid_deal['dealID'] = 'VALID123'
        
        mock_response = Mock()
        mock_response.json.return_value = [invalid_deal, valid_deal]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        out = StringIO()
        call_command('fetch_deals', '--deals-only', stdout=out)
        
        # Verify valid deal was created despite invalid one
        self.assertEqual(Deal.objects.count(), 1)
        deal = Deal.objects.get(deal_id='VALID123')
        self.assertEqual(deal.title, 'Test Game')
        
        output = out.getvalue()
        self.assertIn('Error processing deal INVALID', output)
        self.assertIn('Created deal: Test Game', output)