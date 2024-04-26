from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, Category
from .serializers import OrderSerializer, CategorySerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("Authenticated user:", self.request.user)
        if self.request.user.is_authenticated:
            serializer.save(creator=self.request.user)
        else:
            print("User is not authenticated")

    def get_queryset(self):
        return Order.objects.filter(executor__isnull=True)


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(executor=self.request.user)


