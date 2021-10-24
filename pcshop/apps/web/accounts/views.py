#from threading import Thread

from django.contrib                                     import messages
from django.contrib.auth                                import login, logout
from django.shortcuts                                   import render, redirect
from django.views.generic                               import View

from .forms                                             import UserLoginForm, UserRegisterForm
from .input                                             import input_post_input
from pcshop.apps.web.store.lib                                      import products as product_lib


class UserRegisterView(View):
    template_name = 'apps/accounts/register.html'

    def get(self, request, **kwargs):

        data = product_lib.carData(request)

        cartItems = data['cartItems']

        form= UserLoginForm

        context = {
            'cartItems ': cartItems,
            'register_form': UserRegisterForm,
        }

        return render(self.request, self.template_name, context)

    def post(self, request, **kwargs):

        i = input_post_input(self)

        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)

            new_user.username  = new_user.email
            new_user.is_active = True
            new_user.last_updated_by = new_user.username

            new_user.save()

            messages.success(request, "You are successfuly created your account.")

            return redirect("accounts:login")

        messages.warning(request, "You did not register please try again.")

        context = {
            'i'             : i,
            'page_name'     : 'home',
            'register_form' : form,
        }

        return render(self.request, self.template_name, context)


class UserLoginView(View):
    template_name = 'apps/accounts/login.html'

    def get(self, request, **kwargs):

        data = product_lib.carData(request)

        cartItems = data['cartItems']

        login_form    = UserLoginForm

        context = {
            'cartItems ': cartItems,
            'login'     : 'login',
            'login_form'    : login_form,
        }

        return render(self.request, self.template_name, context)

    def post(self, request, **kwargs):

        data = product_lib.carData(request)

        cartItems = data['cartItems']

        form = UserLoginForm(request.POST or None)

        if form.is_valid():

            user_obj = form.cleaned_data.get('user_obj')

            login(request, user_obj)

            messages.success(request, f"Welcome!, {(user_obj.fullname).title()}, to PARIS COLLECTION.")
            return redirect('store:home')

        messages.warning(request, "You are not login please check your credentials.")

        context ={'login_form': form, 'cartItems': cartItems}
        return render(self.request, self.template_name, context)


class UserLogoutView(View):
    template_name = 'apps/home/index.html'

    def get(self, request, **kwargs):

        logout(request)

        messages.info(request, f" You are loged out . Have a nice day !.")

        return redirect('store:home')