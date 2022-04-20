import django_filters
from .models import Item


class ItemFilter(django_filters.FilterSet):
    CHOICES = (
        ('4GB', '4'),
        ('8GB', '8'),
        ('16GB', '16')
    )
    ordering = django_filters.ChoiceFilter(label='RAM', choices=CHOICES, method='filter_by_ordering')

    class Meta:
        model = Item
        fields = ['price', 'chip']


