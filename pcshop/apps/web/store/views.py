import json
import datetime

from django.db.models import Q
from django.http                                                    import JsonResponse
from django.contrib                                                 import messages
from django.core.paginator                                          import Paginator
from django.views.decorators.csrf                                   import csrf_exempt
from django.shortcuts                                               import render, redirect
from django.contrib.auth                                            import get_user_model

from .models                                                   import Order, Product, OrderItem, ShippingAddress
from .utils                                                    import cookieCart, carData, guestOrder


User = get_user_model()


def store(request):
    template_name = 'apps/store/index.html'

    data = carData(request)

    cartItems = data['cartItems']

    products = Product.objects.all().order_by("title")

    """ Search """

    q = request.GET.get("q")
    if q != "" and q is not None:
        products =  products.filter(
            Q( title__icontains=q) |
            Q(description__icontains=q)|
            Q(price__icontains=q) |
            Q(discount_price__icontains=q)|
            Q(top_featured__icontains=q)|
            Q(best_seller__icontains=q)
        )

    """ pagination """

    paginator = Paginator(products , 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {'products':  page_obj, 'cartItems': cartItems}

    return render(request, template_name, context)


def cart(request):
    template_name = 'apps/store/cart.html'

    data = carData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}

    return render(request, template_name, context)


def updateitem(request):

    data = json.loads(request.body)

    productId = data['productId']

    action = data['action']

    #print('product json ',productId, 'action',action)

    custom = request.user.customer

    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=custom, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)# if it already exist we want to change the value not create a new one

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if  orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def checkout(request):
    template_name = 'apps/store/checkout.html'

    data = carData(request)

    cartItems   = data['cartItems']
    order       = data['order']
    items       = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}

    return render(request, template_name, context)


@csrf_exempt
def processOrder(request):

    #print("data:", request.body)

    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:

        custom = request.user.customer

        order, created = Order.objects.get_or_create(customer=custom, complete=False)

    else:

        custom, order = guestOrder(request, data)

    total = float(data['form']['total'])  # we need to get form value in body we stringify   body:JSON.stringify({ 'form':userFormData, 'shipping':shippingInfo})

    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):  # if the front end total == backend total / may be intruder can manipulate the total in front end
        order.complete = True
    order.save()

    if order.shipping == True:

        ShippingAddress.objects.create(

            customer    = custom,
            order       = order,
            address     = data['shipping']['address'],
            city        = data['shipping']['city'],
            state       = data['shipping']['state'],
            zipcode     = data['shipping']['zipcode'],

        )

    return JsonResponse("Payment submitted....", safe=False)