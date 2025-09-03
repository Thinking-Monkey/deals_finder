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
                self.fetch_deals()
            elif options['stores_only']:
                self.fetch_stores()
            else:
                # Fetch both stores and deals
                self.fetch_stores()
                self.fetch_deals()
            
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
    
    def fetch_deals(self):
        
        ids = '1,7,11'
        dealsNum = 16

        # Fetch deals data from CheapShark API
        self.stdout.write(f'Fetching deals data for stores Steam(id 1), GOG(id 7), Humble Store(id 11)....')
        
        
        try:
            url = f'https://www.cheapshark.com/api/1.0/deals?storeID={ids}&pageSize={dealsNum}'
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
                                int(deal_data['releaseDate']), tz=timezone.get_current_timezone()
                            )
                        except (ValueError, TypeError):
                            pass
                    
                    last_change = None
                    if deal_data.get('lastChange') and deal_data['lastChange'] != '0':
                        try:
                            last_change = datetime.fromtimestamp(
                                int(deal_data['lastChange']), tz=timezone.get_current_timezone()
                            )
                        except (ValueError, TypeError):
                            pass
                    
                    defaults = {
                        'thumb': deal_data.get('thumb', ''),
                        'title': deal_data.get('title', ''),
                        'store': store_obj,
                        'store_name': store_obj.store_name,
                        'sale_price': Decimal(str(deal_data.get('salePrice', 0))),
                        'normal_price': Decimal(str(deal_data.get('normalPrice', 0))),
                        'deal_rating': Decimal(str(deal_data.get('dealRating', 0))),
                        'metacritic_score': int(deal_data['metacriticScore']) if deal_data.get('metacriticScore') else None,
                        'release_date': release_date,
                        'last_change': last_change,
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