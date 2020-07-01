from django.db import models
from django.contrib.auth.models import User

class UserRegistration(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_merchant = models.BooleanField(default = False, blank = True)
    address = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null = True)
    state = models.CharField(max_length=50)
    house_no = models.CharField(max_length=50, null = True)
    area = models.CharField(max_length=100, null = True)
    wait_time=models.CharField(max_length=10, null=True)
    slots=models.CharField(max_length=1200,null=True,default='{"Date":"01-01-2000"}')
    
    def __str__(self):
        return self.user.username

class Product(models.Model):
    merchant = models.ForeignKey('UserRegistration', on_delete=models.CASCADE, null = True)
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300, null = True)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")
    

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=50,default="")
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    user = models.ForeignKey('UserRegistration', on_delete=models.CASCADE, null = True, related_name='usernames')
    is_delivery = models.BooleanField(default = False, blank = True)
    time = models.DateTimeField(null=True)
    est_time = models.DateTimeField(null=True)
    order_status = models.CharField(max_length=50, default="Action Pending", null=True)
    # merchant = models.IntegerField(null = True)
    merchant = models.ForeignKey('UserRegistration', on_delete = models.CASCADE, null =True,related_name='merchant')
    price=models.IntegerField(default=0,null=True)


class SearchModel(models.Model):
    address = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null = True)
    state = models.CharField(max_length=50)
    