from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import F, Window
from django.db.models.functions import RowNumber

from .models import DFUser, Store, Deal
from .serializers import (
    DFUserSerializer, LoginSerializer, StoreSerializer, 
    DealSerializer, DealPublicSerializer
)

class RegisterView(generics.CreateAPIView):
    serializer_class = DFUserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if(DFUser.objects.all()).count() == 0:
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
    try:
        serializer.is_valid(raise_exception=True)
    except Exception as e:
        return JsonResponse({'error': "Credentials are not valid."}, status=400)

    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': DFUserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    user = request.user
    if(user.is_superuser is True):
        return JsonResponse({'error': "You can't remove admin account."}, status=400)
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

    if not request.user.is_authenticated:
        deals= Deal.objects.annotate(
            row_number=Window(
            expression=RowNumber(),
            partition_by=[F('store')],
            order_by='created_at')
            ).filter(row_number__lte=1)
        
        if deals.exists():
            serializer = DealPublicSerializer(deals, many=True)
        else:
            serializer = DealPublicSerializer([], many=True)
        
        return Response({
            'authenticated': False,
            'count': len(serializer.data),
            'deals': serializer.data
        })
    else:
        deals = Deal.objects.all()

        # Utenti autenticati: tutti i deals con paginazione
        # Ogni pagina conterrà 8 elementi per rimanere coerente con
        # la richiesta della parte FE
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
                'hasNext': end < deals.count(),
                'deals': serializer.data
            })
        except ValueError:
            return Response({'error': 'Parametro page non valido'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deals_list_filtered(request):

    deals = Deal.objects.all()

    store = request.GET.get('store')
    if store:
        deals = deals.filter(store__store_name=store)
    
    min_price = request.GET.get('min_price')
    if min_price:
        deals = deals.filter(sale_price__gte=float(min_price))
    
    ordering = request.GET.get('ordering', '-deal_rating')
    allowed_orderings = [
        'deal_rating', '-deal_rating',
        'sale_price', '-sale_price',
        'normal_price', '-normal_price',
        'title', '-title',
        'created_at', '-created_at',
        'metacritic_score', '-metacritic_score'
    ]
    
    if ordering in allowed_orderings:
        deals = deals.order_by(ordering)
    else:
        deals = deals.order_by('-deal_rating')
    
    # Pagination
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 8)
    
    try:
        page = int(page)
        page_size = min(int(page_size), 50)  # Max 50 items per page
        
        start = (page - 1) * page_size
        end = start + page_size
        
        total_count = deals.count()
        paginated_deals = deals[start:end]
        serializer = DealSerializer(paginated_deals, many=True)
        
        return Response({
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
            'has_next': end < total_count,
            'has_previous': page > 1,
            'deals': serializer.data,
            'filters_applied': {
                'store': store,
                'min_price': min_price,
                'ordering': ordering
            }
        })
        
    except ValueError:
        return Response({'error': 'Invalid page or page_size parameter'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deal_detail(request):
    """
    Dettagli di un singolo deal
    """
    deal_id = request.GET.get('deal_id')
    if not deal_id:
        return JsonResponse({'error': 'deal_id parameter required'}, status=400)

    deal = get_object_or_404(Deal, deal_id=deal_id)
    
    serializer = DealSerializer(deal)
    return Response({
        'deal': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filters_data(request):
    from django.db.models import Min, Max
    
    stores = Deal.objects.values('store_name').values_list('store_name', flat=True )
    stores = set(stores)
    list(dict.fromkeys(stores))
    sale_prices = Deal.objects.values('sale_price').values_list('sale_price', flat=True )
    sale_prices = sorted(set(sale_prices))

    return Response({
        'stores': list(stores),
        'prices': list(sale_prices),
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def admin_exist(request):
    """
    Verifica che non ci siano profili registrati
    """
    users = DFUser.objects.all()
    if not users:
        return Response({
            'adminExist': False
        })
    else:
        return Response({
            'adminExist': True
        })