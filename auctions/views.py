from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import NewListingForm, AddCommentForm
from django.template import loader

from .models import User, AuctionCategory, AuctionListing, Bid, Comment



def index(request):
    active_listings = AuctionListing.objects.all().filter(active=True)
    return render(request, "auctions/index.html", {
        'active_listings': active_listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required
def new_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['categories']
            starting_bid = form.cleaned_data['starting_bid']
            image = form.cleaned_data['image']
            currency = form.cleaned_data['currency']

            listing = AuctionListing(
                user=request.user, 
                title=title, 
                description=description,
                category=category,
                bid=starting_bid,
                image=image,
                currency = currency
            )

            bid = Bid(value=starting_bid, listing=listing, user=request.user)

            listing.save()    
            bid.save()
        else:
            return render(request, 'auctions/new_listing.html', {
                'form': form,
            })

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/new_listing.html", {
            'form': NewListingForm(),
        }) 


def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    user_last_bid = 0
    if (request.user.is_authenticated and listing.al_bids.filter(user=request.user).exists()):
        user_last_bid = listing.al_bids.filter(user=request.user).order_by('-id').first().value

    return render(request, 'auctions/listing_page.html', {
        'listing': listing,
        'add_comment_form': AddCommentForm(),
        'al_comments': listing.al_comments.all().order_by('-id'),
        'user_last_bid': user_last_bid,
    })

@login_required
def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)

        if request.user not in listing.w_users.all():
            listing.w_users.add(request.user)

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required
def remove_from_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)

        if request.user in listing.w_users.all():
            listing.w_users.remove(request.user)

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse('index'))
    

@login_required
def bid(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)
        bid_value = request.POST['bid']

        if int(bid_value) > listing.bid:
            listing.bid = bid_value
            bid = Bid(value=bid_value, listing=listing, user=request.user)

            listing.save()
            bid.save()
        else:
            return render(request, 'auctions/listing_page.html', {
                'listing': listing,
                'on_watch': request.user in listing.w_users.all(),
                'message': 'Bid must be higher than current bid.'
            })

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse('index'))
    
@login_required
def close_listing(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)

        highest_bidder = listing.al_bids.order_by('-value').first().user

        if (highest_bidder != listing.user):
            listing.winner = highest_bidder

        for user in listing.w_users.all():
            if user != highest_bidder:
                listing.w_users.remove(user)

        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse('index'))
    
@login_required
def delete_listing(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)

        if (request.user == listing.user):
            listing.delete()

    return HttpResponseRedirect(reverse('index'))

@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)
        content = request.POST['comment']

        comment = Comment(user=request.user, listing=listing, content=content)
        comment.save()

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse('index'))
    

@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)

        if (request.user == comment.user):
            comment.delete()

        return HttpResponseRedirect(reverse('listing_page', args=(comment.listing.id,)))
    else:
        return HttpResponseRedirect(reverse('index'))

            

@login_required
def my_listings(request):
    return render(request, 'auctions/my_listings.html')

@login_required
def watchlist(request):
    return render(request, 'auctions/watchlist.html')

@login_required
def won_listings(request):
    return render(request, 'auctions/won_listings.html')


def categories(request, category):
    
    if(AuctionCategory.objects.filter(name=category).exists()):
        listings = AuctionListing.objects.all().filter(category__name=category)

        return render(request, 'auctions/categories.html', {
            'category': category,
            'listings': listings,
        })
    else:
        return HttpResponseRedirect(reverse('index'))