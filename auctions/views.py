from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# Index page with all the listings
def index(request):
    to_diaplay = AuctionListing.objects.filter(active=True)
    closed_listing = AuctionListing.objects.filter(active=False)
    
    #get all of the categories for nav
    categories = []
    for i in range(1,len(CATEGORY_CHOICE)):
        categories.append(CATEGORY_CHOICE[i][0])
    
    categories.append(CATEGORY_CHOICE[0][0])
    
    return render(request, "auctions/index.html",{
        "auction_listing" : to_diaplay,
        "closed_listing" : closed_listing,
        "categories" : categories,
        "current_category" : "All listings"
    })

# Page for a selected category by user
def category(request, category):
    to_display = AuctionListing.objects.filter(category=category, active=True)
    closed_listing = AuctionListing.objects.filter(category=category, active=False)
    
    #get all of the categories for nav
    categories = []
    for i in range(1,len(CATEGORY_CHOICE)):
        categories.append(CATEGORY_CHOICE[i][0])
    
    categories.append(CATEGORY_CHOICE[0][0])
    
    return render(request, "auctions/index.html",{
        "auction_listing" : to_display,
        "closed_listing" : closed_listing,
        "categories" : categories,
        "current_category" : str(category)
    })
    
# Login the new User and reverse to index if it was successfull
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

# Log out the current user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register a new user
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

# Create a new listing 
@login_required
def new_listing(request):
    if request.method == "POST":
        recieved_form = NewListing(request.POST, request.FILES)
        if recieved_form.is_valid():
            
            #Take info from the form then input the current user, then saves the listing
            listing_model = recieved_form.save(commit=False)
            listing_model.user = request.user
            listing_model.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_listing.html",{
            "listing_form" : NewListing(),
            "error" : True
            })
                
    return render(request, "auctions/new_listing.html",{
        "listing_form" : NewListing(),
        "bids_form" : NewBid()
    })

# Display the listing selected by the user
def listing(request, listing_id):
    
    # Get current listin by id and info about the current user 
    # (Is listing in watchlist, is user the creator, is user a winner)
    current_listing = AuctionListing.objects.get(id=listing_id)
    comments = current_listing.comments.all()
    bids = current_listing.bids.all()
    last_bid = bids.filter(current=True).first()
    is_watchlist = (request.user in current_listing.watchlist.all())
    is_creator = (current_listing.user == request.user)
    is_winner = False
    is_last_bid = False
    
    last_bid = bids.filter(current=True).first()
    # If Current bid is made by the current user and the aiction is closed the current user is the winner
    # If not 
    if(last_bid != None):
        if(not current_listing.active):
            is_winner = (request.user == last_bid.user)
        elif(last_bid.user == request.user):
            is_last_bid = True
            

    if request.method == "POST":
        recieved_bid = NewBid(request.POST)
        
        if(recieved_bid.is_valid()):
            
            # Make sure that the bid is Bigger than the current bid or equals to the start bid
            number =  recieved_bid.cleaned_data['bid']
            if(current_listing.anyBids):
                is_bigger = (number > current_listing.price)
            else:
                is_bigger = (number >= current_listing.price)
            
            # Update the models if the bid is larger
            if(is_bigger):     
                bid_model = recieved_bid.save(commit=False)
                bid_model.user = request.user
                bid_model.listing = current_listing
                bid_model.save()
                
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                
            else:
                return render(request, "auctions/listing.html", {
                "list" : current_listing,
                "comments" : comments,
                "creator" : is_creator,
                "inList" : is_watchlist,  
                "lastBid" : is_last_bid,                  
                "bidForm" : NewBid(),
                "comment_form" : NewComment(),
                "error" : True,
                "error_message" : "Your bid must be bigger than the current one or equal to the starting bid"
                }) 
                
        else:
            return render(request, "auctions/listing.html", {
                "list" : current_listing,
                "comments" : comments,
                "creator" : is_creator,
                "inList" : is_watchlist,
                "lastBid" : is_last_bid,                   
                "bidForm" : NewBid(),
                "comment_form" : NewComment(),
                "error" : True,
                "error_message" : "Make Sure you input a walid number"
                }) 
            
    return render(request, "auctions/listing.html", {
        "list" : current_listing,
        "comments" : comments,
        "creator" : is_creator,
        "inList" : is_watchlist,
        "winner" : is_winner,
        "lastBid" : is_last_bid,  
        "bidForm" : NewBid(),
        "comment_form" : NewComment()
        })

# Display the watchlist of the current user 
@login_required
def watchlist(request):
    user = request.user
    watch_list = user.userwatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "watch_list" : watch_list
    })
    
# Add the listing into the watch list and then redirect into the listing page
def addWatchlist(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    listing.watchlist.add(request.user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
# Remove the listing from the watch list and then redirect into the listing page
def removeWatchlist(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    listing.watchlist.remove(request.user)
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# Close the listing if you are the creato of the listing
def diactivate(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# Add the commnet into the current listing and updates the listing page 
def addComment(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    recieved_comment = NewComment(request.POST)
    
    # Add information about the current listing and the user
    comment_model = recieved_comment.save(commit=False)
    comment_model.user = request.user
    comment_model.listing = listing
    comment_model.save()
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))