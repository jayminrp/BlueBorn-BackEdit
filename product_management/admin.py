from django.contrib import admin
from product_management.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'price', 'color', 'size')  # ✅ แสดงรายการสินค้า
    search_fields = ('product_id', 'product_name')  # ✅ ค้นหาจาก product_id และชื่อ
    list_filter = ('color', 'size')  # ✅ ฟิลเตอร์ง่าย ๆ
    ordering = ('product_id',)  # ✅ เรียงตาม product_id
