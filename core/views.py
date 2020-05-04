from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order

class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def checkout(request):
    return render(request, 'checkout-page.html')

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(item=item,
                                                 user=request.user,
                                                 is_ordered=False)[0]
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'item quantity updated')
        else:
            order.items.add(order_item)
            messages.info(request, 'item added!')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'item added!')
    return redirect('core:product', slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                 user=request.user,
                                                 is_ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, 'item removed!')
            return redirect('core:product', slug=slug)
        else:
            messages.info(request, 'item not found in cart!')
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, 'The user dont have an order')
        return redirect('core:product', slug=slug)

