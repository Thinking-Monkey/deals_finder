from django.db import models

# models.py
from django.db import models
from django.utils import timezone
from datetime import datetime
from decimal import Decimal


class GameDeal(models.Model):

    deal_id = models.CharField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    store_id = models.CharField(max_length=10)

    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    savings = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentuale di sconto")
    deal_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    metacritic_link = models.URLField(blank=True, null=True)
    metacritic_score = models.PositiveSmallIntegerField(blank=True, null=True)
    steam_rating_text = models.CharField(max_length=50, blank=True, null=True)
    steam_rating_percent = models.PositiveSmallIntegerField(blank=True, null=True)
    steam_rating_count = models.PositiveIntegerField(blank=True, null=True)

    release_date = models.DateTimeField(blank=True, null=True)


    thumb = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'game_deals'
        ordering = ['-deal_rating', '-savings']
        indexes = [
            models.Index(fields=['is_on_sale', '-savings']),
            models.Index(fields=['store_id', '-deal_rating']),
        ]
        verbose_name = 'Game Deal'
        verbose_name_plural = 'Game Deals'

    def __str__(self):
        return f"{self.title} - ${self.sale_price}"

    # @property
    # def savings_amount(self):
    #     """Calcola l'importo risparmiato"""
    #     return self.normal_price - self.sale_price

    # @property
    # def is_good_deal(self):
    #     """Considera un buon affare se sconto > 50% e rating > 8.0"""
    #     return self.savings >= 50 and (self.deal_rating or 0) >= 8.0

    # @property
    # def steam_rating_category(self):
    #     """Restituisce la categoria del rating Steam"""
    #     if not self.steam_rating_percent:
    #         return None
        
    #     percent = self.steam_rating_percent
    #     if percent >= 95:
    #         return "Overwhelmingly Positive"
    #     elif percent >= 80:
    #         return "Very Positive"
    #     elif percent >= 70:
    #         return "Mostly Positive"
    #     elif percent >= 40:
    #         return "Mixed"
    #     else:
    #         return "Negative"

    @classmethod
    def from_json(cls, json_data):
        """Crea un'istanza GameDeal da dati JSON"""
        # Conversione timestamp Unix a datetime
        release_date = None
        if json_data.get('releaseDate'):
            release_date = datetime.fromtimestamp(int(json_data['releaseDate']))
        
        last_change = None
        if json_data.get('lastChange'):
            last_change = datetime.fromtimestamp(int(json_data['lastChange']))
        
        return cls(
            internal_name=json_data.get('internalName', ''),
            title=json_data.get('title', ''),
            metacritic_link=json_data.get('metacriticLink'),
            deal_id=json_data.get('dealID', ''),
            store_id=json_data.get('storeID', ''),
            game_id=json_data.get('gameID', ''),
            sale_price=Decimal(json_data.get('salePrice', '0')),
            normal_price=Decimal(json_data.get('normalPrice', '0')),
            is_on_sale=json_data.get('isOnSale') == '1',
            savings=Decimal(json_data.get('savings', '0')),
            metacritic_score=int(json_data['metacriticScore']) if json_data.get('metacriticScore') else None,
            steam_rating_text=json_data.get('steamRatingText'),
            steam_rating_percent=int(json_data['steamRatingPercent']) if json_data.get('steamRatingPercent') else None,
            steam_rating_count=int(json_data['steamRatingCount']) if json_data.get('steamRatingCount') else None,
            steam_app_id=json_data.get('steamAppID'),
            release_date=release_date,
            last_change=last_change,
            deal_rating=Decimal(json_data['dealRating']) if json_data.get('dealRating') else None,
            thumb=json_data.get('thumb')
        )
    
    class GameDealHistory(models.Model):
        internal_name = models.CharField(max_length=255, db_index=True)
        title = models.CharField(max_length=255)
        game_id = models.CharField(max_length=50, db_index=True)
        steam_app_id = models.CharField(max_length=50, blank=True, null=True, db_index=True)

        deal_id = models.CharField(max_length=255, unique=True, db_index=True)
        store_id = models.CharField(max_length=10)

        sale_price = models.DecimalField(max_digits=10, decimal_places=2)
        normal_price = models.DecimalField(max_digits=10, decimal_places=2)
        is_on_sale = models.BooleanField(default=False)
        savings = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentuale di sconto")
        deal_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

        metacritic_link = models.URLField(blank=True, null=True)
        metacritic_score = models.PositiveSmallIntegerField(blank=True, null=True)
        steam_rating_text = models.CharField(max_length=50, blank=True, null=True)
        steam_rating_percent = models.PositiveSmallIntegerField(blank=True, null=True)
        steam_rating_count = models.PositiveIntegerField(blank=True, null=True)

        release_date = models.DateTimeField(blank=True, null=True)
        last_change = models.DateTimeField(blank=True, null=True)

        thumb = models.URLField(blank=True, null=True)

        created_at = models.DateTimeField(auto_now_add=True)
        archived_at = models.DateTimeField(default=timezone.now)

        class Meta:
            db_table = 'game_deals_h'
            ordering = ['-archived_at']
            indexes = [
                models.Index(fields=['is_on_sale', '-savings']),
                models.Index(fields=['store_id', '-deal_rating']),
            ]
            verbose_name = 'Game Deal'
            verbose_name_plural = 'Game Deals'

        def __str__(self):
            return f"{self.title} - ${self.sale_price}"

    class FetchSchedule(models.Model):
        """Configurazione per il fetch automatico"""
        name = models.CharField(max_length=255, unique=True)
        hours_interval = models.IntegerField(help_text="Intervallo in ore tra i fetch")
        api_endpoint = models.URLField()
        is_active = models.BooleanField(default=True)
        last_fetch = models.DateTimeField(null=True, blank=True)
    
    def is_due(self):
        if not self.last_fetch:
            return True
        next_fetch = self.last_fetch + timezone.timedelta(hours=self.hours_interval)
        return timezone.now() >= next_fetch