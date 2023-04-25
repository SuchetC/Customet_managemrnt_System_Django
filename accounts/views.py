from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .  models import *
from . forms import OrderForm , CreateUserForm ,CustomerForm
from . filters import  OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , allowed_users , admin_only
from django.contrib.auth.models import  Group

# Create your views here.



@login_required(login_url='login')
@admin_only
def home(request):
    orders = order.objects.all()

    customers = customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered =  orders.filter(status='Delivered').count()
    ofdelivery = orders.filter(status='out for delivery').count()
    pending = orders.filter(status= 'pending').count()

    context = {'orders': orders, 'customers': customers ,'total_customers':total_customers ,'total_orders':total_orders
               , 'delivered':delivered ,'ofdelivery':ofdelivery, 'pending': pending }

    return render(request , 'accounts/dashboard.html' , context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = product.objects.all()
    return render(request , 'accounts/products.html' ,{'products' : products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def cust(request , pk_test):

    cutomer = customer.objects.get(id=pk_test)
    orders = cutomer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET , queryset=orders)
    orders = myFilter.qs

    context = {'cutomer': cutomer , 'orders':orders ,'order_count':order_count , 'myFilter':myFilter}
    return render(request , 'accounts/customers.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(customer , order ,fields=('product' , 'status') , extra=10)
    cutomer = customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=order.objects.none() ,instance=cutomer)
    #form = OrderForm(initial={'cutomer': cutomer})
    if request.method == 'POST':
        # print("printing" , request.POST)
        #form = OrderForm(request.POST)

        formset = OrderFormSet(request.POST ,instance=cutomer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset' : formset}
    return render(request , 'accounts/order_form.html' ,context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request , pk):
    orders = order.objects.get(id=pk)
    form = OrderForm(instance=orders)
    if request.method == 'POST':

        form = OrderForm(request.POST,instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')


    context = {'form' : form }
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request , pk):
    orders = order.objects.get(id=pk)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')

    context = {'item' : orders}
    return render(request, 'accounts/delete.html', context)



@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            email= form.cleaned_data.get('email')

            group = Group.objects.get(name='customer')
            user.groups.add(group)


            customer.objects.create(user=user, name=username,email=email)

            messages.success(request, 'Succesfully created ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username , password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request , 'Username or Password is incorrect')


    context = {}

    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()


    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    ofdelivery = orders.filter(status='out for delivery').count()
    pending = orders.filter(status='pending').count()

    # print('ORDERS' , orders)

    context = { 'orders':orders , 'total_orders':total_orders , 'delivered':delivered ,'ofdelivery':ofdelivery ,'pending':pending }
    return render(request , 'accounts/user.html' , context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    cust = request.user.customer
    form = CustomerForm(instance=cust)

    if request.method == 'POSt':
        form = CustomerForm(request.POST ,request.FILES , instance=cust)
        if form.is_valid():
            form.save()

    context = { 'form':form}

    return render(request, 'accounts/account_settings.html', context)

