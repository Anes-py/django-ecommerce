from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    color = forms.CharField(required=False)
    size = forms.CharField(required=False)
