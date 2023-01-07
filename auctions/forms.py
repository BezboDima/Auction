from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class NewListing(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['name', 'discription', 'price', 'category', 'image']
        widgets = {
            'name' : forms.TextInput(attrs={'class' : "form-control col-lg-9 col-md-10"}),
            'discription' : forms.Textarea(attrs={'class' : "form-control col-lg-9 col-md-10"}),
            'price' : forms.NumberInput(attrs={'class' : "form-control col-lg-9 col-md-10"})
        }

class NewBid(forms.ModelForm):
    
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid' : forms.NumberInput(attrs={ 'class' : "form-control", 'style': 'border-color: blue;' })
        }
    # Changes the description of the form to None
    def __init__(self, *args, **kwargs):
            super(NewBid, self).__init__(*args, **kwargs)
            self.fields['bid'].label = ""

class NewComment(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment' : forms.Textarea(attrs={'class' : "form-control col-lg-9 col-md-10", 'rows': 4})
        }
    # Changes the description of the form to Write new comment
    def __init__(self, *args, **kwargs):
        super(NewComment, self).__init__(*args, **kwargs)
        self.fields['comment'].label = "Write new comment"