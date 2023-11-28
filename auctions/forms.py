from django import forms
from .models import AuctionCategory

class NewListingForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="Title*", 
        max_length=128, 
        widget=forms.TextInput(attrs={
            'id': 'title',
            'name': 'title'
        }))
    
    description = forms.CharField(
        required=False,
        label="Description", 
        widget=forms.Textarea(attrs={
            'id': 'description', 'name': 'description'
        }))

    categories = forms.ModelChoiceField(
        required=False,
        queryset = AuctionCategory.objects.all(), 
        label="Categories", 
        widget=forms.Select(attrs={
            'id': 'category',
            'name': 'category'
        }))

    starting_bid = forms.FloatField(
        required=True,
        label="Starting Bid*", 
        widget=forms.NumberInput(attrs={
            'id': 'starting-bid',
            'name': 'starting-bid'
        }))

    image = forms.ImageField(
        required=False,
        label="Image", 
        widget=forms.FileInput(attrs={
            'id': 'image',
            'name': 'image'
        }))



class WForm(forms.Form):
    pass

