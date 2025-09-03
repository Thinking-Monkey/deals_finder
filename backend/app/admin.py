from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DFUser, Store, Deal


@admin.register(DFUser)
class DFUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informazioni personali', {'fields': ('first_name', 'last_name')}),
        ('Permessi', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date importanti', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'store_name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('store_name',)
    ordering = ('store_id',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'sale_price', 'normal_price', 'savings', 'deal_rating', 'is_on_sale', 'created_at')
    list_filter = ('is_on_sale', 'store', 'created_at', 'metacritic_score')
    search_fields = ('title', 'internal_name', 'deal_id')
    ordering = ('-deal_rating', 'sale_price')
    readonly_fields = ('created_at', 'updated_at', 'deal_id')
    
    fieldsets = (
        ('Informazioni base', {
            'fields': ('deal_id', 'title', 'internal_name', 'store', 'game_id')
        }),
        ('Prezzi e sconti', {
            'fields': ('sale_price', 'normal_price', 'is_on_sale', 'savings', 'deal_rating')
        }),
        ('Valutazioni', {
            'fields': ('metacritic_score', 'steam_rating_text', 'steam_rating_percent', 'steam_rating_count')
        }),
        ('Dettagli tecnici', {
            'fields': ('steam_app_id', 'thumb', 'release_date', 'last_change')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )