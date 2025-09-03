from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
import random

from .models import DFUser, Store, Deal
from .serializers import (
    DFUserSerializer, LoginSerializer, StoreSerializer, 
    DealSerializer, DealPublicSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = DFUser.objects.all()
    serializer_class = DFUserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if(queryset := DFUser.objects.all()).count() == 0:
            # Se non ci sono utenti, il primo ad iscriversi diventa admin
            user = serializer.save(is_superuser=True)
        else:
            user = serializer.save()
        
        # Genera i token JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': DFUserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


# View per il login che restituisce, nel caso l'utente esista e la password sia corretta, un token JWT che
# vale un'ora e un refresh token che vale 1 giorno, l'API accetta solo richieste POST con username e password
# e non richiede autenticazione per essere chiamata
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': DFUserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # Aggiunge il token alla blacklist
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    user = request.user
    if(user.is_superuser is True):
        raise PermissionError({'error': "You can't remove admin account."})
    else:
        user.delete()
        return Response({'message': 'Account deleted successfully.'}, 
                        status=status.HTTP_200_OK)

# API che restituiscono i deals e gli store, con differenziazione tra utenti autenticati e non autenticati
@api_view(['GET'])
@permission_classes([AllowAny])
def deals_list(request):

    # API che restituisce deals di gog, steam e humble bundle in base all'autenticazione:
    # - Utenti non autenticati: i 3 migliori deals per negozio con informazioni limitate, solo per creare la card
    # - Utenti autenticati: tutti i deals con informazioni complete, con paginazione a 8 deal per pagina
    deals = Deal.objects.all()
    
    if not request.user.is_authenticated:
        # Utenti non autenticati: i migliori 3 deals per negozio, uno per negozio
        if deals.exists():
            random_deals = random.sample(list(deals), min(3, deals.count()))
            serializer = DealPublicSerializer(random_deals, many=True)
        else:
            serializer = DealPublicSerializer([], many=True)
        
        return Response({
            'authenticated': False,
            'count': len(serializer.data),
            'deals': serializer.data
        })
    else:
        # Utenti autenticati: tutti i deals con paginazione
        page = request.GET.get('page', 1)
        page_size = 8
        
        try:
            page = int(page)
            start = (page - 1) * page_size
            end = start + page_size
            
            paginated_deals = deals[start:end]
            serializer = DealSerializer(paginated_deals, many=True)
            
            return Response({
                'authenticated': True,
                'count': deals.count(),
                'page': page,
                'page_size': page_size,
                'has_next': end < deals.count(),
                'deals': serializer.data
            })
        except ValueError:
            return Response({'error': 'Parametro page non valido'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deal_detail(request, deal_id):
    """
    Dettagli di un singolo deal
    """
    deal = get_object_or_404(Deal, deal_id=deal_id)
    
    if not request.user.is_authenticated:
        serializer = DealPublicSerializer(deal)
        return Response({
            'authenticated': False,
            'deal': serializer.data
        })
    else:
        serializer = DealSerializer(deal)
        return Response({
            'authenticated': True,
            'deal': serializer.data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Profilo dell'utente autenticato
    """
    serializer = DFUserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_fetch_deals_async(request):
    """
    Endpoint per triggere il comando fetch_deals in modalità asincrona
    Utile per operazioni lunghe che non bloccano il frontend
    """
    import threading
    from django.core.management import call_command
    from django.core.management.base import CommandError
    import logging
    
    # Parametri dal request
    stores_only = request.data.get('stores_only', False)
    deals_only = request.data.get('deals_only', False)
    max_price = request.data.get('max_price', 15)
    store_id = request.data.get('store_id', 1)
    
    # Validazione parametri
    try:
        max_price = float(max_price)
        store_id = int(store_id)
    except (ValueError, TypeError):
        return Response({
            'success': False,
            'error': 'Parametri max_price o store_id non validi'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def run_fetch_command():
        """Funzione per eseguire il comando in background"""
        try:
            command_args = [
                f'--max-price={max_price}',
                f'--store-id={store_id}'
            ]
            
            if stores_only:
                command_args.append('--stores-only')
            elif deals_only:
                command_args.append('--deals-only')
            
            call_command('fetch_deals', *command_args)
            logging.info(f'Fetch deals command completed successfully for user {request.user.username}')
            
        except Exception as e:
            logging.error(f'Error in async fetch deals: {str(e)}')
    
    # Avvia il comando in un thread separato
    thread = threading.Thread(target=run_fetch_command)
    thread.daemon = True
    thread.start()
    
    return Response({
        'success': True,
        'message': 'Comando fetch_deals avviato in background',
        'note': 'Il comando è in esecuzione. Controlla i log per lo stato.',
        'parameters': {
            'stores_only': stores_only,
            'deals_only': deals_only,
            'max_price': max_price,
            'store_id': store_id
        }
    })