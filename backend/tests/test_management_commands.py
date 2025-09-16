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
            mock_response.raise