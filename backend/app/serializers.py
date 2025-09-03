from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import DFUser, Store, Deal

    
class DFUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    passwordCheck = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = DFUser
        fields = ('username', 'password', 'passwordCheck')

        # Dicitura di Django Rest Framework usata per aggiungere keyword argument 
        # che funzionano da vincoli ai campi del serializer
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True},
            'passwordCheck': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['passwordCheck']:
            raise serializers.ValidationError({"Passwords does not match."})
        attrs.pop('passwordCheck')  # Rimuove passwordCheck dai dati validati perché non serve più
        return attrs
    
    def create(self, validated_data):
        if(validated_data.get('is_superuser') is True):
            validated_data["is_staff"] = True
            user = DFUser.objects.create_user(**validated_data)
            return user
        else:
            user = DFUser.objects.create_user(**validated_data)
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenziali non valide.')
            if not user.is_active:
                raise serializers.ValidationError('Account disattivato.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Username e password sono richiesti.')
        
        return attrs

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     passwordCheck = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'passwordCheck')
#         extra_kwargs = {
#             'username': {'required': True}
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['passwordCheck']:
#             raise serializers.ValidationError({"password": "Passwords does not match."})

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             usename=validated_data['usename']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    
    class Meta:
        model = Deal
        fields = '__all__'


class DealPublicSerializer(serializers.ModelSerializer):
    """Serializer per utenti non autenticati - mostra solo informazioni base per disegnare la card"""
    store_name = serializers.CharField(source='store.store_name', read_only=True)
    
    class Meta:
        model = Deal
        fields = (
            'deal_id', 'title', 'store_name', 'sale_price', 'normal_price', 
            'thumb'
        )