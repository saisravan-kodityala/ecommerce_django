from django.contrib import admin

# Register your models here.
from .models import Category, Products, Customer, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'date', 'price', 'quantity', 'status')
    list_editable = ('status',)
    list_filter = ('status', 'date')
    search_fields = ('customer__email', 'product__name')
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Customer)
admin.site.register(Order)
