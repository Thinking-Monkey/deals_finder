import requests
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import Store, Deal


class Command(BaseCommand):
    help = 'Fetch deals and stores data from CheapShark API'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--complete',
            action='complete'
            help='Fetch complete data (stores and deals), usefull the first time',
        parser.add_argument(
            '--stores-only',
            action='store_true',
            help='Fetch only stores data',
        )
        parser.add_argument(
            '--deals-only',
            action='store_true',
            help='Fetch only deals data',
        )
    
    def handle(self, *args, **options):
        try:
            if options['deals_only']:
                self.fetch_deals(options['store_id'], options['max_price'])
            elif options['stores_only']:
                self.fetch_stores()
            else:
                # Fetch both stores and deals
                self.fetch_stores()
                self.fetch_deals(options['store_id'], options['max_price'])
            
            self.stdout.write(
                self.style.SUCCESS('Successfully completed data fetch')
            )
        except Exception as e:
            raise CommandError(f'Error during data fetch: {str(e)}')
    
    def fetch_stores(self):
        """Fetch stores data from CheapShark API"""
        self.stdout.write('Fetching stores data...')
        
        try:
            response = requests.get('https://www.cheapshark.com/api/1.0/stores')
            response.raise_for_status()
            stores_data = response.json()
            
            created_count = 0
            updated_count = 0
            
            for store_data in stores_data:
                store_id = int(store_data['storeID'])
                defaults = {
                    'store_name': store_data['storeName'],
                    'is_active': store_data['isActive'] == 1,
                    'images': store_data.get('images', {}),
                }
                
                store, created = Store.objects.update_or_create(
                    store_id=store_id,
                    defaults=defaults
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created store: {store.store_name}')
                else:
                    updated_count += 1
                    self.stdout.write(f'Updated store: {store.store_name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Stores fetch completed: {created_count} created, {updated_count} updated'
                )
            )
            
        except requests.RequestException as e:
            raise CommandError(f'Error fetching stores: {str(e)}')
        except Exception as e:
            raise CommandError(f'Error processing stores data: {str(e)}')
    
    def fetch_deals(self, store_id, max_price):
        """Fetch deals data from CheapShark API"""
        self.stdout.write(f'Fetching deals data for store {store_id} with max price ${max_price}...')
        
        try:
            url = f'https://www.cheapshark.com/api/1.0/deals?storeID={store_id}&upperPrice={max_price}'
            response = requests.get(url)
            response.raise_for_status()
            deals_data = response.json()
            
            created_count = 0
            updated_count = 0
            
            for deal_data in deals_data:
                try:
                    # Assicuriamoci che lo store esista
                    store_obj, _ = Store.objects.get_or_create(
                        store_id=int(deal_data['storeID']),
                        defaults={
                            'store_name': f"Store {deal_data['storeID']}",
                            'is_active': True,
                            'images': {}
                        }
                    )
                    
                    # Prepara i dati per il deal
                    release_date = None
                    if deal_data.get('releaseDate') and deal_data['releaseDate'] != '0':
                        try:
                            release_date = datetime.fromtimestamp(
                                int(deal_data['releaseDate']), tz=timezone.utc
                            )
                        except (ValueError, TypeError):
                            pass
                    
                    last_change = None
                    if deal_data.get('lastChange') and deal_data['lastChange'] != '0':
                        try:
                            last_change = datetime.fromtimestamp(
                                int(deal_data['lastChange']), tz=timezone.utc
                            )
                        except (ValueError, TypeError):
                            pass
                    
                    defaults = {
                        'internal_name': deal_data.get('internalName', ''),
                        'title': deal_data.get('title', ''),
                        'store': store_obj,
                        'game_id': deal_data.get('gameID', ''),
                        'sale_price': Decimal(str(deal_data.get('salePrice', 0))),
                        'normal_price': Decimal(str(deal_data.get('normalPrice', 0))),
                        'is_on_sale': deal_data.get('isOnSale', '0') == '1',
                        'savings': Decimal(str(deal_data.get('savings', 0))),
                        'metacritic_score': int(deal_data['metacriticScore']) if deal_data.get('metacriticScore') else None,
                        'steam_rating_text': deal_data.get('steamRatingText', ''),
                        'steam_rating_percent': int(deal_data['steamRatingPercent']) if deal_data.get('steamRatingPercent') else None,
                        'steam_rating_count': int(deal_data['steamRatingCount']) if deal_data.get('steamRatingCount') else None,
                        'steam_app_id': deal_data.get('steamAppID', ''),
                        'release_date': release_date,
                        'last_change': last_change,
                        'deal_rating': Decimal(str(deal_data.get('dealRating', 0))),
                        'thumb': deal_data.get('thumb', ''),
                    }
                    
                    deal, created = Deal.objects.update_or_create(
                        deal_id=deal_data['dealID'],
                        defaults=defaults
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f'Created deal: {deal.title}')
                    else:
                        updated_count += 1
                        self.stdout.write(f'Updated deal: {deal.title}')
                
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error processing deal {deal_data.get("dealID", "unknown")}: {str(e)}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Deals fetch completed: {created_count} created, {updated_count} updated'
                )
            )
            
        except requests.RequestException as e:
            raise CommandError(f'Error fetching deals: {str(e)}')
        except Exception as e:
            raise CommandError(f'Error processing deals data: {str(e)}')
    
    def parse_timestamp(self, timestamp_str):
        """Parse timestamp from string"""
        if not timestamp_str or timestamp_str == '0':
            return None
        try:
            return datetime.fromtimestamp(int(timestamp_str), tz=timezone.utc)
        except (ValueError, TypeError):
            return None