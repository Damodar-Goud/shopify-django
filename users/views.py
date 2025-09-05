from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer


# -------------------------
# REGISTER
# -------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]  # ✅ anyone can register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------LoginView
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("🚀 LoginView HIT:", request.data)

        email = request.data.get("email")
        password = request.data.get("password")

        print("🚀 Login attempt:", email, password)

        # check if user exists
        try:
            user_obj = User.objects.get(email=email)
            print("✅ Found user in DB:", user_obj.email)
            print("🔑 Password valid?", user_obj.check_password(password))
        except User.DoesNotExist:
            print("❌ No user with that email")

        user = authenticate(request, email=email, password=password)
        print("🎯 authenticate() returned:", user)

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": {"id": user.id, "email": user.email, "username": user.username},
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# -------------------------
# LOGOUT
# -------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ only logged-in users

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ needs SimpleJWT blacklist app
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
