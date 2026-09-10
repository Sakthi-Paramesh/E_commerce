from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'}),
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review title'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review...'}),
        }


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address_line1 = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Street Address, Building, Apartment'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    pincode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN Code'}))
    country = forms.CharField(max_length=100, initial='India',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    payment_method = forms.ChoiceField(
        choices=[('cod', 'Cash on Delivery'), ('online', 'Online Payment'), ('upi', 'UPI'), ('card', 'Card Payment')],
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'}),
        initial='cod',
    )
    notes = forms.CharField(required=False,
                             widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Order notes (optional)'}))


class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search products...',
        'id': 'search-input',
    }))
