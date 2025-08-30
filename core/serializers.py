from rest_framework import exceptions, serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from dj_rest_auth.models import TokenModel
from dj_rest_auth.serializers import TokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from .utils import RedisTokenManager



User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = str(attrs.get('email')).lower()
        password = attrs.get('password')

        if email and password:
            # First check if user exists
            user = self.get_auth_user(email, password)
            
            if not user:
                user_exists = User.objects.filter(email=email).exists()
                if user_exists:
                    msg = {"Invalid password": "Please try again."}
                else:
                    msg = {"Invalid email": "Account with this email does not exist."}
                raise exceptions.ValidationError(msg)
            
            # Now check activation status
            if not user.is_active:
                msg = {"Inactive account": "This account has been deactivated, please contact admin."}
                raise exceptions.ValidationError(msg)
        else:
            msg = {"Invalid credentials": "Must include email and password."}
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def get_auth_user(self, email, password):
        """
        Helper method to authenticate user using Django's authentication backend.
        Returns None if authentication fails.
        """
        try:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            return user
        except Exception as e:
            return None

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'email', 'full_name')
        model = User

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    token = serializers.SerializerMethodField(method_name='tokens')
    class Meta:
        model = TokenModel
        fields = ('user', 'token',)

    def tokens(self, request):
        refresh = TokenObtainPairSerializer().get_token(request.user)
        access = AccessToken().for_user(request.user)
        data = {
            "refresh": str(refresh),
            "access": str(access)
        }
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            #validators=[UniqueValidator(queryset=User.objects.all())]
            )
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'password2')
        extra_kwargs = {
            'full_name': {'required': True},
            'email': {'required': True}
        }

    

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['email'] = str(instance.email).lower()
        return data

    
    def validate_email(self, value):
        try:
            get_user_model().objects.get(email=value.lower())
        except ObjectDoesNotExist:
            # Good to go
            pass
        else:
            # Email in use
            raise serializers.ValidationError("Email already exists")

        return value
    

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        email = validated_data['email'].lower()
        user = User.objects.create(
            email=email,
            username=email,  # Set username to email
            full_name=validated_data['full_name'],
            password=make_password(validated_data['password2'])
        )
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self):
        email = self.validated_data['email']
        token = RedisTokenManager.generate_password_reset_token(email)
        return {'token': token, 'email': email}


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Verify token and get associated email
        email = RedisTokenManager.verify_password_reset_token(attrs['token'])
        if not email:
            raise serializers.ValidationError({"token": "Invalid or expired password reset token."})

        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid token - user not found."})

        return attrs

    def save(self):
        password = self.validated_data['new_password']
        self.user.set_password(password)
        self.user.save()
        return self.user