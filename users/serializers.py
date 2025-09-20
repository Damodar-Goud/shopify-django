from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "password2", "role"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # ✅ hash the password
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        # Try email login
        from django.contrib.auth import get_user_model

        User = get_user_model()
        try:
            user = User.objects.get(email=username_or_email)
            username_or_email = user.username
        except User.DoesNotExist:
            pass  # keep as username

        attrs["username"] = username_or_email
        return super().validate(attrs)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid credentials"})

        # Call parent validate with username
        data = super().validate(
            {
                "username": user.username,  # ✅ map email → username for SimpleJWT
                "password": password,
            }
        )
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Optional: add custom claims
        token["email"] = user.email
        token["role"] = getattr(user, "role", None)
        return token
