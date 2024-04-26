from django.contrib import admin

from .models import Order, Category, UserProfile

admin.site.register(Order)

admin.site.register(Category)

admin.site.register(UserProfile)

