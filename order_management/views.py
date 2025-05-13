# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import OrderSerializer

# class OrderCreateView(APIView):
#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Order created successfully!"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# order_management/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # ตรวจสอบว่า request.data มีข้อมูลทั้งหมดที่ต้องการ
            order_data = request.data

            required_fields = ['customer_name', 'location', 'total_price', 'items']
            for field in required_fields:
                if field not in order_data:
                    return Response({"error": f"Missing {field} field."}, status=status.HTTP_400_BAD_REQUEST)

            # ตรวจสอบแต่ละรายการใน 'items'
            for item in order_data['items']:
                if 'product_name' not in item or 'price' not in item or 'quantity' not in item:
                    return Response({"error": "Missing product details in items."}, status=status.HTTP_400_BAD_REQUEST)

            # สร้าง order และ order items
            order = Order.objects.create(
                customer_name=order_data['customer_name'],
                location=order_data['location'],
                note=order_data.get('note', ''),
                total_price=order_data['total_price'],
            )

            for item in order_data['items']:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['product_name'],
                    price=item['price'],
                    quantity=item['quantity'],
                    image_url=item['image_url']
                )

            return Response({"message": "Order created successfully!"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderDetailView(APIView):
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
