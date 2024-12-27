from django import forms
from django.forms import NumberInput


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=NumberInput(
            attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1
            }
        )
    )