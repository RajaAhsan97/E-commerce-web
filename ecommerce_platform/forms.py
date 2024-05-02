
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password_confirm']:
            raise ValidationError("Your password does not match")
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class CategoryCreateForm(forms.Form):
    category_name = forms.CharField(label="Category", max_length=50)
    image = forms.ImageField(label="Image")

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs['placeholder'] = 'Category name...'

class ProductAddForm(forms.Form):
    category = forms.CharField(label="Category", max_length=50)
    product_nm = forms.CharField(label="Product name", max_length=50)
    description = forms.CharField(label="Description", max_length=1000, widget=forms.Textarea())
    image = forms.ImageField(label="Image")
    price = forms.IntegerField(label="Price")

    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['product_nm'].widget.attrs['placeholder'] = 'Product name...'
        self.fields['description'].widget.attrs['placeholder'] = 'Product description...'

class ProductSpecsAddForm(forms.Form):
    spec_type = forms.CharField(label="Specification Type", max_length=50)
    spec_value = forms.CharField(label="Specification Value", max_length=50)