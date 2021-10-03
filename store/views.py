import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from store.models import Order, Product, OrderItem


def store(request):
    template_name = 'store/index.html'

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user,
            complete=False
        )

        items = order.orderitem_set.all()
        print(items)

        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'sipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all().order_by("title")

    context = {'products': products, 'cartItems': cartItems}

    return render(request, template_name, context)



def cart(request):
    template_name = 'store/cart.html'

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user = user,
            complete = False
        )

        items = order.orderitem_set.all()
        #print(items)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0, 'sipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}

    return render(request, template_name, context)


#@csrf_exempt
def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('product json ',productId, 'action',action)

    user = request.user

    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)# if it already exist we want to change the value not create a new one

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity -= 1

    if action == 'delete':
        orderItem.delete()

    orderItem.save()

    if  orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def checkout(request):
    template_name = 'store/checkout.html'

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user = user,
            complete = False
        )

        items = order.orderitem_set.all()
        #print(items)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0, 'sipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}

    return render(request, template_name, context)


def processOrder(request):
    print("data:", request.body)

    return JsonResponse("Payment submitted....", safe=False)