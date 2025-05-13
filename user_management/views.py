# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from product_management.models import Product
from .models import Favorite
from django.shortcuts import get_object_or_404

class ToggleFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, product_id=product_id)

        favorite, created = Favorite.objects.get_or_create(user=user, product=product)

        if not created:
            # กด unfavorite
            favorite.delete()
            return Response({'status': 'unfavorited'})
        else:
            return Response({'status': 'favorited'})
        

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        product_data = []
        
        for product in products:
            # เช็คว่าสินค้าไหนที่ผู้ใช้ favorite
            is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()
            product_data.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'is_favorited': is_favorited,
            })

        return Response(product_data)
# accounts/views.py

class FavoriteListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ดึงสินค้าที่ถูก favorite โดยผู้ใช้
        favorites = Favorite.objects.filter(user=request.user)
        favorite_products = []

        for favorite in favorites:
            product = favorite.product
            favorite_products.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'price': float(product.price),
                'color': product.color,
                'description': product.description,
                'size': product.size,
            })

        return Response(favorite_products)


# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Custom Login View (with extra user info)
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# User Profile View
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        full_name = f"{user.first_name} {user.last_name}".strip()
        return Response({
            "username": user.username,
            "full_name": full_name,
            "email": user.email,
        })

# Logout View (blacklist refresh token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
