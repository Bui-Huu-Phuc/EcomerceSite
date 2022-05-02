from django import forms
from django.forms import widgets

from items.models import Item

colors = (
    ('Đen', 'Đen'),
)
PAYMENT_CHOICES = (
    ('IB', 'Internet Banking'),
    ('C', 'COD')
)


class OrderItemForm(forms.Form):
    item_color = forms.ChoiceField(choices=colors, widget=forms.RadioSelect(attrs={'require': True}))

