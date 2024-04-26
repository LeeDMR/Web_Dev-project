from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=[('executor', 'Executor'), ('client', 'Client')])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s profile - Role: {self.role}, Balance: {self.balance}"

    def add_balance(user_profile, amount):
        user_profile.balance += amount
        user_profile.save()

    def subtract_balance(user_profile, amount):
        if user_profile.balance >= amount:
            user_profile.balance -= amount
            user_profile.save()
        else:
            raise ValueError("Insufficient funds")
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Order(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='orders_created', null=True, blank=True, on_delete=models.CASCADE)
    executor = models.ForeignKey(User, related_name='orders_executed', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='open')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    reward = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)

class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='transactions_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='transactions_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')



