import json
from django.contrib                                                 import messages
from django.contrib.auth import get_user_model
from django.db.models                                   import Q

from pcshop.apps.web.store.models                                                        import *

User = get_user_model()

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []

    order = {'get_cart_total': 0, 'get_cart_items': 0, 'sipping': False}

    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems   += cart[i]["quantity"]

            product     = Product.objects.get(id=i)

            total       = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total

            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id'        : product.id,
                    'title'     : product.title,
                    'price'     : product.price,
                    'image_url' : product.image_url
                },
                'quantity'  : cart[i]['quantity'],
                'get_total' : total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass

    return {'cartItems':cartItems, 'order': order, 'items': items}


def  carData(request):

    if request.user.is_authenticated:

        custom          = request.user

        order, created  = Order.objects.get_or_create(customer=custom, complete=False)

        items = order.orderitem_set.all()

        cartItems = order.get_cart_items

    else:

        cookieData = cookieCart(request)

        cartItems = cookieData['cartItems']

        order = cookieData['order']

        items = cookieData['items']

    return {'cartItems':cartItems, 'order': order, 'items': items}


def guestOrder(request, data):

    name = data['form']['name']

    email = data['form']['email']

    cookieData = cookieCart(request)

    items = cookieData['items']

    custom, created = User.objects.get_or_create(email=email)
    custom.username = name
    custom.save()

    order = Order.objects.create(customer= custom, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    return custom, order


def get_top_featured_product():

    featured_product = Product.objects.exclude(
        Q(best_seller=True)|
        Q(bool_deleted=True)
    ).values('id', 'code', 'slug','label','category','title', 'digital','image' ,'description',
            'price','discount_price','top_featured','best_seller', 'datetime_created', 'datetime_updated',
            'time_updated', 'last_updated_by', 'publish','bool_deleted')

    return featured_product


def get_best_seller_product():

    best_product = Product.objects.exclude(
        Q(top_featured=True)|
        Q(bool_deleted=True)
    ).values('id', 'code', 'slug','label','category','title', 'digital','image' ,'description',
            'price','discount_price','top_featured','best_seller', 'datetime_created', 'datetime_updated',
            'time_updated', 'last_updated_by', 'publish','bool_deleted')

    return best_product


def get_all_product():

    all_product = Product.objects.exclude(
        Q(bool_deleted=True)
    ) \
        .values('id', 'code', 'slug', 'label', 'category', 'title', 'digital', 'image',
                'description',
                'price', 'discount_price', 'top_featured', 'best_seller', 'datetime_created', 'datetime_updated',
                'time_updated', 'last_updated_by', 'publish', 'bool_deleted').order_by('title')

    return all_product