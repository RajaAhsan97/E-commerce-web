from django import forms

class CartForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    address = forms.CharField(max_length=500)
    contact = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Name...'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Delivery Address...'
        self.fields['contact'].widget.attrs['placeholder'] = 'Enter your contact number...'