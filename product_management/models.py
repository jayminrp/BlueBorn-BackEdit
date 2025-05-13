from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"