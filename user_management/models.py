from django.db import models
from django.contrib.auth.models import User

# models.py ของ app ใหม่หรือ user_management (หรือรวมไว้ใน product_management ก็ได้)
from django.contrib.auth.models import User  # หรือใช้ get_user_model() ถ้า custom user
from django.db import models
from product_management.models import Product

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # คนหนึ่ง favorite สินค้าเดิมซ้ำไม่ได้

    def __str__(self):
        return f"{self.user.username} likes {self.product.product_name}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} x {self.quantity}"