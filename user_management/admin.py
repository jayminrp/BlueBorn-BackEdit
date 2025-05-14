from django.contrib import admin
from user_management.models import User, CartItem

# Register your models here.

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')  # ✅ แสดงรายการสินค้า

