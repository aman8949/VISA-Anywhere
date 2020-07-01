from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as login_user
from .models import Product, Contact, Order, UserRegistration,SearchModel
from math import ceil
from django.urls import reverse, reverse_lazy
from .forms import UserForm, UserRegistrationForm
import datetime
from datetime import timedelta
import requests
import urllib.parse
import json
from django.http import JsonResponse
from .VISA_MSearch import *
from .VISA_Queue import *


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


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
            profile.address = profile.house_no + ", " + profile.area
            profile.user = user
            test = 'shop/templates/shop/test.json'
            with open(test, 'r') as fileHandler2:
                test_str=fileHandler2.read()
                profile.slots=test_str
            profile.save()
            if profile.is_merchant:
                address = str(profile.area)+", "+ str(profile.city) +", "+ str(profile.zipcode)
                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                response = requests.get(url).json()
                resp={}
                resp['lat']=response[0]['lat']
                resp['lon']=response[0]['lon']
                resp['zipcode']=profile.zipcode
                resp['id'] = profile.id
                resp['name'] = profile.name
                resp['address'] = profile.address
                resp['phone'] = profile.phone
                #merchant_list.append(resp)
                jsonFile = 'shop/templates/shop/data.json'
                # Open a json file for writing json data
                data = json.load(open(jsonFile))
                if type(data) is dict:
                    data = [data]
                data.append(resp)
                print(data)
                with open(jsonFile, 'w') as fileHandler1:
                    json.dump(data, fileHandler1, indent = 2)
                
                    
            return HttpResponseRedirect(reverse('shop:login'))
        else:
            print(user_form.errors)

    # if request.method == 'GET':
    else:
        mer = UserRegistration.objects.filter(user_id=request.user.id).first()
        if request.user.is_authenticated and mer.is_merchant == False:
            return HttpResponseRedirect(reverse('shop:merchant_list'))
        elif request.user.is_authenticated and mer.is_merchant == True:
            return HttpResponseRedirect(reverse('shop:merchant_homepage'))
        else:
            user_form = UserForm()
            profile_form = UserRegistrationForm()

    return render(request, 'shop/register.html', {'user_form': user_form, 'profile_form': profile_form})



def home(request):
    return HttpResponseRedirect(reverse('shop:register'))


def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            login_user(request, user)
            user_profile = UserRegistration.objects.filter(
                user_id=request.user.id).first()
            if user_profile.is_merchant:
                return HttpResponseRedirect(reverse('shop:merchant_homepage'))
            else:
                return HttpResponseRedirect(reverse('shop:merchant_list'))
        else:
            messages.add_message(request, messages.ERROR,
                                 "Invalid password. Please try again.")
            return HttpResponseRedirect(reverse('shop:login'))
    else:
        mer = UserRegistration.objects.filter(user_id=request.user.id).first()
        if request.user.is_authenticated and mer.is_merchant == False:
            return HttpResponseRedirect(reverse('shop:merchant_list'))
        elif request.user.is_authenticated and mer.is_merchant == True:
            return HttpResponseRedirect(reverse('shop:merchant_homepage'))
        return render(request, 'shop/login.html')

# Merchant Homepage


@login_required
def merchant_homepage(request):
    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    h=False
    for cat in cats:
        merchant = UserRegistration.objects.filter(
            user_id=request.user.id).first()
        prod = Product.objects.filter(category=cat, merchant_id=merchant.id)
        n = len(prod)
        nSlides = n//4+ceil(n/4-(n//4))
        if nSlides>0 :
            h=True
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, 'h':h}
    return render(request, 'shop/merchant_homepage.html', params)

# Merchant Product Delete


@login_required
def product_delete(request, product_id):
    Product.objects.filter(product_id=product_id).delete()
    return HttpResponseRedirect(reverse('shop:merchant_homepage'))

# Merchant Product Add


@login_required
def product_add(request):
    if request.method == 'POST':
        merchant = UserRegistration.objects.filter(
            user_id=request.user.id).first()
        new_product = Product(product_name=request.POST['name'],
                              category=request.POST['category'],
                              subcategory=request.POST['subcategory'],
                              price=request.POST['price'],
                              desc=request.POST['desc'],
                              pub_date=datetime.datetime.now(),
                              image=request.FILES['image'],
                              merchant_id=merchant.id)
        new_product.save()
        return HttpResponseRedirect(reverse('shop:merchant_homepage'))
    else:
        return render(request, 'shop/merchant_add.html')


@login_required
def merchant_list(request):
    
    date=datetime.datetime.now().strftime("%d-%m-%Y")
    dt=datetime.datetime.now().strftime("%Y-%m-%d")
    user = UserRegistration.objects.filter(user_id=request.user.id).first()
    merchant_l = UserRegistration.objects.filter(is_merchant=True, zipcode=user.zipcode)
    dic = {}
    for mer in merchant_l:
        data = json.loads(mer.slots)
        test_str=data
        if data['Date']!=str(date):
            # print(data["Date"])
            # print(str(date))
            test = 'shop/templates/shop/test.json'
            with open(test, 'r') as fileHandler2:
                test_str=fileHandler2.read()
                test_str = json.loads(test_str)
                test_str['Date']=date
            mer.slots=json.dumps(test_str)
        for temp in test_str:
            if temp > str(datetime.datetime.now().strftime("%H:%M")) and test_str[temp] < "9" and temp!= "Date":
                dic[mer.id] = datetime.datetime.strptime(temp, "%H:%M") - datetime.datetime.strptime(str(datetime.datetime.now().strftime("%H:%M")), "%H:%M")
                mer.wait_time = dic[mer.id] 
                mer.save()
                break
        
        
    mer_que=[]
    if user.zipcode=="94306" or user.zipcode=="94105":
        r=json.loads(merchantQueue())
        for item in r['responseData']['merchantList']:
                address = str(item['city'])+", "+ str(item['state']) +", " +str(item['country']) +", "+ str(item['zip'])
                url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
                response = requests.get(url).json()
                resp={}
                resp['lat']=response[0]['lat']
                resp['lon']=response[0]['lon']
                resp['zipcode']=str(item['zip'])
                resp['id'] = str(item['feedbackCorrelationID'])
                resp['name'] = str(item['name'])
                resp['address'] = address
                resp['wait_time'] = str(item['waitTime'])
                #merchant_list.append(resp)
                mer_que.append(resp)
                
        jsonFile = 'shop/templates/shop/data_queue.json'
                # Open a json file for writing json data
        with open(jsonFile, 'w') as outfile:
            json.dump(mer_que, outfile)
    address = str(user.area) +", "+ str(user.city)+ ", "+ str(user.zipcode)
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    return render(request, 'shop/mapbox.html', {'zipcode': user.zipcode,
                                                 'lat': response[0]['lat'],
                                                 'lon': response[0]['lon'],
                                                 'merchant':dic})

@login_required
def merchant_list2(request):
    user = UserRegistration.objects.filter(user_id=request.user.id).first()
    merchant_l = UserRegistration.objects.filter(
        is_merchant=True, zipcode=user.zipcode)
    return render(request, 'shop/merchant_list.html', {'merchant_list': merchant_l})

#@login_required
def product_list(request,merchant_id):
    allProds=[]
    catprods= Product.objects.values('category','product_id')
    cats={item['category'] for item in catprods}
    h=False
    for cat in cats:
        prod=Product.objects.filter(category=cat,merchant_id=merchant_id)
        n=len(prod)
        nSlides=n//4+ceil(n/4-(n//4))
        if nSlides > 0:
            h=True
        allProds.append([prod, range(1,nSlides), nSlides])
    params = {'allProds':allProds,'h':h}
    return render(request,'shop/index.html',params)

def searchMatchProduct(query,item):
    if query in item.product_name or query in item.desc or query in item.category or query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower() or query in item.product_name.upper() or query in item.desc.upper() or query in item.category.upper():
        return True
    else:
        return False

def searchMatchMerchant(query,merchant):
    if query in merchant.name or query in merchant.name.lower() or query in merchant.name.upper():
        return True
    else:
        return False

@login_required
def search(request):
    query = request.GET.get('search')

    if len(query) <= 2 :
        params = {'msg': "Please make sure to enter relevant search query"}
        return render(request, 'shop/search.html', params)

    allMerc=[]
    user = UserRegistration.objects.filter(user_id=request.user.id).first()
    merchants = UserRegistration.objects.filter(is_merchant=True, zipcode=user.zipcode)
    for mer in merchants:
        if searchMatchMerchant(query,mer):
            allMerc.append(mer)
    
    allVisaMerc=[]
    result=json.loads(merchantSearch(query,"94132"))
    stata=result["merchantLocatorServiceResponse"]["status"]["statusCode"]
    if(stata=="CDI000" or stata == "CDI000MAXRCW"):
        merc=SearchModel()
        info=result["merchantLocatorServiceResponse"]["response"][0]["responseValues"]
        merc.name=info["visaMerchantName"]
        merc.address=info["merchantStreetAddress"]+", "+info["merchantCity"]+", "+info["merchantState"]+", "+info["merchantPostalCode"]
        allVisaMerc.append(merc)
        del merc

    allProdsMerc=[]
    catprods= Product.objects.values('category','product_id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod_temp=Product.objects.filter(category=cat)
        prod = [ item for item in prod_temp if searchMatchProduct(query,item)]
        n=len(prod)
        nSlides=n//4+ceil(n/4-(n//4))

        if len(prod)!=0:
            allProdsMerc.append(prod[0].merchant)

    

    
    params = {'allProdMerc': allProdsMerc, "msg": "",'merchant_list':allMerc,'VISA_merchant':allVisaMerc}
    if len(allProdsMerc) == 0 and len(allMerc) == 0 and len(allVisaMerc) == 0:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


@login_required
def checkout(request, merchant_id):
    merchant = UserRegistration.objects.filter(id=merchant_id).first()
    date=datetime.datetime.now().strftime("%d-%m-%Y")
    dt=datetime.datetime.now().strftime("%Y-%m-%d")
    data = json.loads(merchant.slots)
    test_str=data
    if data['Date']!=str(date):
        test = 'shop/templates/shop/test.json'
        with open(test, 'r') as fileHandler2:
            test_str=fileHandler2.read()
            test_str = json.loads(test_str)
            test_str['Date']=date
    time=datetime.datetime.now().strftime("%H:%M")
    time=str(time)
    if request.method == "POST":
        user = UserRegistration.objects.filter(user_id=request.user.id).first()
        items_json = request.POST.get('itemsJson')
        mer_id = request.POST['merid']
        test_str[request.POST['drop'][0:5]]=str(int(test_str[request.POST['drop'][0:5]])+1)
        merchant.slots=json.dumps(test_str, indent = 2)

        data=json.loads(items_json)
        total=0
        for item in data:
            total = total + int(data[item][0])*int(data[item][2])

        thank = True
        order = Order(items_json=items_json, user_id=user.id, is_delivery=(request.POST['is_delivery'] == 'Home Delivery'),
                      est_time=dt+" "+request.POST['drop'][0:5], merchant_id=mer_id, time=datetime.datetime.now(),price=total)
        
        order.save()
        merchant.save()
        return render(request, 'shop/checkout.html', {'merchant_id':merchant_id,'thank': thank})
    #When request method is get
    
    return render(request, 'shop/checkout.html',{'merchant_id':merchant_id,'str':test_str,'time': time})


@login_required
def mer_order_list(request):
    merchant = UserRegistration.objects.filter(user_id=request.user.id).first()
    orders = Order.objects.filter(merchant_id=merchant.id).order_by('-time')
    return render(request, 'shop/mer_order_list.html', {'orders': orders})


@login_required
def mer_order_detail(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()
    if request.method == "POST":
        dt=datetime.datetime.now().strftime("%Y-%m-%d")
        if request.POST['order_status'] == "Accept Order":
            order.order_status = "Approved"
            order.est_time = dt+" "+request.POST['time']
        else:
            order.order_status = "Rejected"
        order.save()
        return HttpResponseRedirect(reverse('shop:mer_order_list'))
    # print(type(order.est_time))
    # str_time = datetime.datetime.strptime(str(order.est_time)[11:16], "%H:%M")
    list_time=[]
    dt=order.est_time + timedelta(hours=5,minutes=30)  
    for i in range(6):
        list_time.append(str(dt+timedelta(minutes=5*i))[11:16])
    return render(request, 'shop/mer_order_detail.html', {'order': order, 'list_time':list_time})


@login_required
def user_order_list(request):
    user = UserRegistration.objects.filter(user_id=request.user.id).first()
    orders = Order.objects.filter(user_id=user.id).order_by('-time')
    return render(request, 'shop/user_order_list.html', {'orders': orders})


@login_required
def user_order_detail(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()
    api_address = 'http://api.openweathermap.org/data/2.5/weather?units=metric&appid=d73a909843bf1ed3e1aa9c6364a8841c&q='
    url = api_address + order.merchant.city
    r = requests.get(url).json()
    city_weather = {
            'city' : order.merchant.city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
    if request.method == "POST" and request.POST['payment']=="success":
        order.order_status = "Payment Successful"
        order.save()
        # print(request.POST['payment'])
    return render(request, 'shop/user_order_detail.html', {'order': order, 'city_weather':city_weather})


def load_json(request):
    return render(request, 'shop/data.json')

def load_queue_json(request):
    return render(request, 'shop/data_queue.json')

