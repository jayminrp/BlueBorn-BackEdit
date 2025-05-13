# product_management/views.py
from django.http import JsonResponse
from .models import Product
from django.db.models import Avg, Count

def product_all(request):
    products = Product.objects.all().values(
        'product_id', 'product_name', 'price', 'color', 'description', 'size', 'image',
    )
    return JsonResponse(list(products), safe=False)

def product_detail(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        data = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'price': float(product.price),
            'color': product.color,
            'description': product.description,
            'size': product.size,
            'image': product.image,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def product_summary(request):
    summary = Product.objects.aggregate(
        total_products=Count('id'),
        avg_price=Avg('price')
    )
    return JsonResponse({
        'total_products': summary['total_products'],
        'avg_price': float(summary['avg_price']) if summary['avg_price'] else 0.0
    })
