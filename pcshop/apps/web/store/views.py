import json
import datetime

from django.db.models                                               import Q
from django.http                                                    import JsonResponse
from django.contrib                                                 import messages
from django.core.paginator                                          import Paginator
from django.views.generic                                           import View
from django.shortcuts                                               import render, redirect
from django.contrib.auth                                            import get_user_model

from pcshop.apps.web.store.forms import GetInTouchForm
from pcshop.apps.web.store.models                                   import Order, Product, OrderItem, ShippingAddress
from pcshop.apps.web.store.lib                                      import products as product_lib
from pcshop.common  import user as check_user

User = get_user_model()


class HomeView(View):
    template_name = 'apps/store/index.html'

    def get(self, request, **kwargs):


        staff = check_user.check_allowed_staff(self)

        data = product_lib.carData(request)

        cartItems = data['cartItems']

        products = product_lib.get_all_product()

        featured_product = product_lib.get_top_featured_product()

        best_product = product_lib.get_best_seller_product()

        """ Search """

        q = request.GET.get("q")
        if q != "" and q is not None:
            products = products.filter(

                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(price__icontains=q) |
                Q(discount_price__icontains=q) |
                Q(top_featured__icontains=q) |
                Q(best_seller__icontains=q)

            )

        """ pagination """

        paginator = Paginator(products, 10)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {'products': page_obj, 'cartItems': cartItems, 'featured_product': featured_product,
                   'best_product': best_product, 'staff': staff, 'page_name': 'home'}

        return render(request, self.template_name, context)


class AddToCartView(View):
    template_name = 'apps/store/cart.html'

    def get(self, request, **kwargs):

        staff = check_user.check_allowed_staff(self)

        data = product_lib.carData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items': items, 'order': order, 'cartItems':cartItems, 'staff': staff, 'page_name': 'cart'}

        return render(request, self.template_name, context)


class UpdateItemView(View):

    def post(self, request, **kwargs):

        data = json.loads(self.request.body)

        productId = data['productId']

        action = data['action']

        custom = request.user

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


class CheckoutView(View):
    template_name = 'apps/store/checkout.html'

    def get(self, request, **kwargs):

        staff = check_user.check_allowed_staff(self)

        data = product_lib.carData(request)

        cartItems   = data['cartItems']
        order       = data['order']
        items       = data['items']

        context = {'items': items, 'order': order, 'cartItems':cartItems, 'staff': staff, 'page_name': 'checkout'}

        return render(request, self.template_name, context)


#@csrf_exempt
class ProcessOrderView(View):

    def post(self, request, **kwargs):

        data = json.loads(self.request.body)

        if request.user.is_authenticated:

            custom = self.request.user

            order, created = Order.objects.get_or_create(customer=custom, complete=False)

        else:

            custom, order = product_lib.guestOrder(request, data)

        total = float(data['form']['total'])  # we need to get form value in body we stringify   body:JSON.stringify({ 'form':userFormData, 'shipping':shippingInfo})

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


class ContactView(View):
    template_name = 'apps/store/contact.html'

    def get(self, request, **kwargs):

        #i = input_get_input(self)

        staff = check_user.check_allowed_staff(self)

        form = GetInTouchForm

        #address = get_address(self)

        context = {
            #'i': i,
            'staff': staff,
            'page_name': 'contact',
            #'address': address,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        form = GetInTouchForm(request.POST or None)

        if form.is_valid():

            GetInTouchForm()

            #email = MakeAppointmentNotificationEmail(obj)
            #email.run()

            message = "Your Appointment is received successfully we send you a confirmation email"
            messages.success(request, message)
            return redirect(self.request.META['HTTP_REFERER'])

        else:
            messages.success(request, "Your contact details failed please try again !")

        context = {
            'form': form
        }

        return render(request, self.template_name, context)