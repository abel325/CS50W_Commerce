from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment, AuctionCategory

# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "bid", "category")


admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(AuctionCategory)
