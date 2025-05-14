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
from .models import CartItem
from .serializers import CartItemSerializer

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
                'image': product.image,
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


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, product_id=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({'message': 'Added to cart'}, status=status.HTTP_200_OK)

    def put(self, request):
        # ✅ Adjust quantity
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or quantity is None:
            return Response({'error': 'Missing product_id or quantity'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(CartItem, user=user, product__product_id=product_id)
        cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({'message': 'Quantity updated'}, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        if product_id:
            # ❌ Remove one item
            item = get_object_or_404(CartItem, user=user, product__product_id=product_id)
            item.delete()
            return Response({'message': 'Removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # ✅ Clear all
            CartItem.objects.filter(user=user).delete()
            return Response({'message': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)
