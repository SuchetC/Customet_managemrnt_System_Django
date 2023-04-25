from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customer(models.Model):
    user = models.OneToOneField(User , null=True , blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250 , null=True)
    phone = models.CharField(max_length=250 , null=True)
    email = models.CharField(max_length=250 , null=True)
    profile_pic = models.ImageField(default= 'Profile-Avatar.png',null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)


    def __str__(self):
        return self.name




class tag(models.Model):
    name = models.CharField(max_length=250 , null=True)

    def __str__(self):
        return self.name

class product(models.Model):
    CATEGORY = (
        ('Indoor' , 'Indoor'),
        ('OutDoor' , 'OutDoor'),
    )

    name = models.CharField(max_length=250 , null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=250 , null=True , choices=CATEGORY)
    description = models.CharField(max_length=250 , null=True , blank = True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    tag = models.ManyToManyField(tag)

    def __str__(self):
        return self.name


class order(models.Model):
    STATUS = (
        ('pending' , 'pending'),
        ('out for delivery' , 'out for delivery'),
        ('Delivered' , 'Delivered'),
    )

    customer = models.ForeignKey(customer , null=True , on_delete=models.SET_NULL)
    product = models.ForeignKey(product , null=True , on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=250 , null=True , choices=STATUS)

    def __str__(self):
        return self.product.name


