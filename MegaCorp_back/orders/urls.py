from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import take_order, register, user_balance_view, user_reviews_view, OrderDeclineView, CompleteOrderView
from .cbv import OrderListCreateAPIView, CategoryListCreateAPIView, UserOrdersView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('', OrderListCreateAPIView.as_view(), name='order_list_create'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:order_id>/take/', take_order, name='take_order'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('register/', register, name='register'),
    path('user/balance/', user_balance_view, name='user-balance'),
    path('user/orders/', UserOrdersView.as_view(), name='user-orders'),
    path('user/reviews/', user_reviews_view, name='user-reviews'),
    path('<int:pk>/decline/', OrderDeclineView.as_view(), name='order-decline'),
    path('<int:pk>/complete/', CompleteOrderView.as_view(), name='order-complete'),

]

#   path('api/orders/', order_list_create, name='order_list_create'),
#    path('user/balance/', user_balance_view, name='user-balance'),
#    path('user/orders/', UserOrdersView.as_view(), name='user-orders'),
#    path('user/reviews/', user_reviews_view, name='user-reviews'),