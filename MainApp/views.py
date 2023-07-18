from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from .models import *


@login_required(login_url='login')
def home(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(name__icontains=q)
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'menu.html', context)

# def category(request):


@login_required(login_url='login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {"product": product}
    return render(request, 'shop-page.html',context)

# def cart(request):
#     user = request.user
#     if request.user.is_authenticated:
#         user = request.user.customer
#         order, created = Order.objects.get_or_create(user = user, complete = False)
#         products = order.orderitem_set.all()
#     else:
#         products = []
#
#     context = {'products': products}
#     return render(request, 'menu.html', context)

def cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user, product = product).save()
    return redirect('/')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    l = cart
    return print(l)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def profile(request):
    user = request.user
    return render(request, 'menu.html', {'user': user})
