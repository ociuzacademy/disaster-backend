from django.db import models

# Create your models here.
class Camp(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    address = models.TextField()
    gmap_link = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    capacity = models.IntegerField()
    contact_person = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='camp_pics/', blank=True, null=True)


    def __str__(self):
        return self.name  # Optional: Adds a string representation for better readability in the admin panel


class CollectionCenter(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    address = models.TextField()
    gmap_link = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_person = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='collect_pics/', blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models

class DisNews(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    news_pic = models.ImageField(upload_to='news_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the time when the object is created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update the time whenever the object is saved

    def __str__(self):
        return self.title
