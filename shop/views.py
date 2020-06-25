from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as login_user
from .models import Product, Contact, Order, UserRegistration
from math import ceil
from django.urls import reverse, reverse_lazy
from .forms import UserForm,UserRegistrationForm
import datetime


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('shop:login'))

def register(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserRegistrationForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Saving directly to DB
            user = user_form.save()
            # Hashing pass
            # user.set_password(user.password)
            # user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('shop:login'))
        else:
            print(user_form.errors)

    # if request.method == 'GET':
    else:
        user_form = UserForm()
        profile_form = UserRegistrationForm()

    return render(request, 'shop/register.html', {'user_form':user_form, 'profile_form' : profile_form})



def home(request):
	return HttpResponseRedirect(reverse('shop:register'))

def login(request):
    if request.method == 'POST':
        user = authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if user is not None:
            login_user(request,user)
            user_profile = UserRegistration.objects.filter(user_id=request.user.id).first()
            if user_profile.is_merchant:
                return HttpResponseRedirect(reverse('shop:merchant_homepage'))
            else:
                return HttpResponseRedirect(reverse('shop:merchant_list'))
        else:
            messages.add_message(request,messages.ERROR,"Invalid password. Please try again.")
            return HttpResponseRedirect(reverse('shop:login'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('shop:merchant_list'))
        else:
            return render(request,'shop/login.html')

@login_required
def merchant_homepage(request):
    allProds=[]
    catprods= Product.objects.values('category','product_id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        merchant = UserRegistration.objects.filter(user_id = request.user.id).first()
        prod=Product.objects.filter(category=cat,merchant_id=merchant.id)
        n=len(prod)
        nSlides=n//4+ceil(n/4-(n//4))
        allProds.append([prod, range(1,nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request,'shop/merchant_homepage.html',params)

@login_required
def product_delete(request,product_id):
    Product.objects.filter(product_id=product_id).delete()
    return HttpResponseRedirect(reverse('shop:merchant_homepage'))

@login_required
def product_add(request):
    if request.method =='POST':
        merchant = UserRegistration.objects.filter(user_id = request.user.id).first()
        new_product = Product(product_name=request.POST['name'],
                              category = request.POST['category'],
                              subcategory = request.POST['subcategory'],
                              price = request.POST['price'],
                              desc = request.POST['desc'],
                              pub_date =datetime.datetime.now() ,
                              image = request.FILES['image'],
                              merchant_id = merchant.id)
        new_product.save()
        return HttpResponseRedirect(reverse('shop:merchant_homepage'))
    else:
        return render(request, 'shop/merchant_add.html')


@login_required
def merchant_list(request):
    user = UserRegistration.objects.filter(user_id=request.user.id).first()
    merchant_list = UserRegistration.objects.filter(is_merchant=True, zipcode=user.zipcode)
    return render(request, 'shop/merchant_list.html', {'merchant_list':merchant_list})

@login_required
def product_list(request,merchant_id):
    allProds=[]
    catprods= Product.objects.values('category','product_id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat,merchant_id=merchant_id)
        n=len(prod)
        nSlides=n//4+ceil(n/4-(n//4))
        allProds.append([prod, range(1,nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request,'shop/index.html',params)

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact= Contact(name=name, email=email,phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

@login_required   
def productView(request, id):
    product=Product.objects.filter(product_id=id)
    return render(request, 'shop/productView.html', {'product':product[0]})

@login_required
def checkout(request):
    if request.method=="POST":
        user = UserRegistration.objects.filter(user_id=request.user.id).first()
        items_json=request.POST.get('itemsJson')
        thank=True
        order=Order(items_json=items_json, user_id=user.id, is_delivery= (request.POST['is_delivery']=='Home Delivery') )
        order.save()
        return render(request, 'shop/checkout.html',{'thank':thank})
    return render(request, 'shop/checkout.html')
    
# Create your views here.
