from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Order, Category, UserProfile, User, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'balance']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.profile.role
        return data

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']
class OrderSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'creator', 'executor', 'status', 'category', 'is_completed', 'reward']

class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    rating = serializers.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    comment = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):

        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.order = validated_data.get('order', instance.order)
        instance.reviewer = validated_data.get('reviewer', instance.reviewer)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class UserProfileSerializer2(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    role = serializers.ChoiceField(choices=[('executor', 'Executor'), ('client', 'Client')])
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):

        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.role = validated_data.get('role', instance.role)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance



