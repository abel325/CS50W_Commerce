from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name="users")

    def __str__(self):
        return f"{self.id}: {self.username}"


class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    w_users = models.ManyToManyField(User, blank=True, related_name="watchlist")
    title = models.CharField(max_length=128)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='pics', null=True)
    category = models.ForeignKey('AuctionCategory', on_delete=models.SET_NULL, null=True, related_name="ac_listings")
    bid = models.FloatField()
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="won_listings")

    def __str__(self):
        return f"{self.id}: {self.title} posted by {self.user.username}"


class Bid(models.Model):
    value = models.FloatField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="al_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")

    def __str__(self):
        return f"{self.id}: {self.value} bid by {self.user.username} on {self.listing.title} auction"
    

class Comment(models.Model):
    pass

class AuctionCategory(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.id}: {self.name}"
        