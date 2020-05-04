from django.contrib import admin
from .models import Item, OrderItem, Order

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity']

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order)