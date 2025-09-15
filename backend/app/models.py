from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone


class DFUserManager(BaseUserManager):
    # Il primo utente registrante passerà di qui ma con is_staff=True e is_superuser=True
    # quindi diventerà admin del sito, gli altri utenti passeranno di qui con
    # **extra_fields vuoti e diventeranno utenti normali
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Username is required')
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class DFUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = DFUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'df_user'
        verbose_name = 'Deal Finder User'
        verbose_name_plural = 'Deal Finder Users'
    
    def __str__(self):
        return self.username


class Store(models.Model):
    store_id = models.IntegerField(unique=True, primary_key=True)
    store_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stores'
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
    
    def __str__(self):
        return f"{self.store_name} ({self.store_id})"


class Deal(models.Model):
    deal_id = models.CharField(max_length=255, unique=True, primary_key=True)
    thumb = models.URLField(blank=True)
    title = models.CharField(max_length=500)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='deals')
    store_name = models.CharField(max_length=30, blank=True)  # Copia del nome dello store per facilità di accesso
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    deal_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    metacritic_score = models.IntegerField(null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    last_change = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'deals'
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
        ordering = ['-deal_rating', 'sale_price']
    
    def __str__(self):
        return f"{self.title} - ${self.sale_price}"