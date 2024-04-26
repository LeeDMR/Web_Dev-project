from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from rest_framework import status, views, response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Order, Review
from .permissions import IsExecutor
from .serializers import OrderSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from .models import UserProfile



#@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
#def order_list_create(request):
#    if request.method == 'GET':
#        orders = Order.objects.all()
#        serializer = OrderSerializer(orders, many=True)
#        return Response(serializer.data)
#    elif request.method == 'POST':
#        serializer = OrderSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save(creator=request.user)
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def take_order(request, order_id):
#    try:
#        order = Order.objects.get(id=order_id, status='open')
#    except Order.DoesNotExist:
#        return Response({'message': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
#    if order.creator != request.user:
#        order.executor = request.user
#        order.status = 'taken'
#        order.save()
#        serializer = OrderSerializer(order)
#        return Response(serializer.data)
#    return Response({'message': 'You cannot take your own order'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role')
    if not username or not password or not role:
        return Response({'error': 'Username, password, and role are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    UserProfile.objects.create(user=user, role=role)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def take_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, status='open')
        order.executor = request.user
        order.status = 'taken'
        order.save()
        return Response({'status': 'order taken'})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews_view(request):
    reviews = Review.objects.filter(reviewer=request.user)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def user_balance_view(request):
    balance = request.user.profile.balance
    return Response({'balance': balance})

class OrderDeclineView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, executor=request.user)
        order.executor = None
        order.status = 'open'
        order.save()
        return response.Response({'message': 'You have successfully declined the order'}, status=status.HTTP_200_OK)


class CompleteOrderView(views.APIView):
    permission_classes = [IsAuthenticated]

    @atomic
    def post(self, request, pk):

        order = get_object_or_404(Order, pk=pk, executor=request.user, is_completed=False)
        order.is_completed = True
        order.save()


        if order.executor:
            order.executor.profile.balance += order.reward
            order.executor.profile.save()
        order.delete()
        return response.Response({'message': 'Order has been marked as completed and payment has been transferred'},
                                 status=status.HTTP_200_OK)


