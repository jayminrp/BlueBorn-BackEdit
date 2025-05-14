from django.db import models


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    note = models.TextField(blank=True, null=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
