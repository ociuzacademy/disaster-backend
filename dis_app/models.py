from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from adminapp.models import *
from disastermanagement import settings


class UserReg(models.Model):
    name = models.CharField(max_length=100,default='')
    email=models.EmailField(max_length=100,default='')
    password=models.CharField(max_length=100,default='')
    address = models.CharField(max_length=100,default='')
    location = models.CharField(max_length=100,default='')
    image = models.ImageField(upload_to='user_image')
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    utype = models.CharField(max_length=100,default='user')
    

class VolunteerCamp(models.Model):
    email=models.EmailField(max_length=100,default='')
    password=models.CharField(max_length=100,default='')
    assigned_camp = models.ForeignKey(Camp, on_delete=models.SET_NULL, null=True, blank=True,related_name='assigned_volunteers')
    name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    aadhaar = models.CharField(max_length=100, default='')
    camp_select = models.ManyToManyField(Camp, related_name='volunteer_selections', blank=True)  # Many-to-Many relationship with Camp
    skills_exp = models.TextField(blank=True, default='')
    status = models.CharField(max_length=100,default="pending")
    utype = models.CharField(max_length=100,default='volcmp')
    def __str__(self):
        return self.name
    
class VolunteerCollectionCentre(models.Model):
    email=models.EmailField(max_length=100,default='')
    password=models.CharField(max_length=100,default='')
    assigned_collection_center = models.ForeignKey(CollectionCenter,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_volunteers')
    name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    aadhaar = models.CharField(max_length=100, default='')
    collection_center_select = models.ManyToManyField(CollectionCenter, related_name='volunteer_selections', blank=True
    )  # Many-to-Many relationship with CollectionCenter
    skills_exp = models.TextField(blank=True, default='')
    status = models.CharField(max_length=100,default="pending")
    utype = models.CharField(max_length=100,default='volcc')
    def __str__(self):
        return self.name



class Resources(models.Model):
    collectioncenter = models.ForeignKey(CollectionCenter,on_delete=models.CASCADE,related_name='resources')
    name = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=100,default='')
    quantity = models.PositiveIntegerField(default=0)
    date_recieved = models.DateTimeField(auto_now_add=True)


class Donations(models.Model):
    collectioncenter = models.ForeignKey(CollectionCenter,on_delete=models.CASCADE,related_name='donations')
    resources = models.ForeignKey(Resources,on_delete=models.CASCADE,related_name='donations')
    name = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=100,default='')
    quantity = models.PositiveIntegerField(default='0')
    date_recieved = models.DateTimeField(auto_now_add=True)

# class Reviews(models.Model):
#     CollectionCenter=models.ForeignKey(CollectionCenter,)