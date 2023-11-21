from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=128)
    description = models.TextField(null=True)
    image = models.BinaryField(null=True) # upload_to parameter may be needed
    category = models.ForeignKey('AuctionCategory', on_delete=models.SET_NULL, null=True, related_name="listings")
    starting_bid = models.FloatField()
    current_bid = models.FloatField()


class Bid(models.Model):
    value = models.FloatField()
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    pass

class Comment(models.Model):
    pass

class AuctionCategory(models.Model):
    name = models.CharField(max_length=64)
    pass
