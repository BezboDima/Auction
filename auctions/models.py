from django.contrib.auth.models import AbstractUser
from django.db import models
CATEGORY_CHOICE = [
    ("Other", "Other"),
    ("Furniture", "Furniture"),
    ("Houses", "Houses")

]


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    discription = models.CharField(max_length=1000)
    category = models.CharField(choices = CATEGORY_CHOICE, default='N/A', max_length=20)
    image = models.ImageField(blank=True, upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    watchlist = models.ManyToManyField(User,blank=True,null=True, related_name="userwatchlist")
    anyBids = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return f"ID: {self.id} Title: {self.name}, Category: {self.category}, UserID: {self.user.id}\nDiscription{self.discription}"
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    current = models.BooleanField(default=False)
    
    # Once the new bid is saved makes sure that it is now a current bid
    def save(self, *args, **kwargs):
        
        bids = Bid.objects.filter(listing = self.listing)
        if self.listing.anyBids:
            previous = bids.filter(current=True).first()
            previous.current = False
            self.current = True
            super (Bid, previous).save(*args, **kwargs)
            super (Bid, self).save(*args, **kwargs)
        else:
            # If auction did not have any bids change it to True
            listing = self.listing
            listing.anyBids = True 
            listing.price = self.bid
            listing.save()
            self.current = True
            super (Bid, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"ID: {self.id} Bid: {self.bid}, ListingID: {self.listing.id}, Made By UserID: {self.user.id}, current: {self.current}"
    
class Comment(models.Model):
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self) -> str:
        return f"ID: {self.id} ListingID: {self.listing.id}, UserID: {self.listing.id}\nComment: {self.comment}"

