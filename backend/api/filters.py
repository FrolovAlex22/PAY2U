import django_filters
from services.models import Service, Subscription


class ServiceFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id')
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Service
        fields = ['category', 'is_featured']


class SubscriptionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr='gte'
    )
    end_date = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr='lte'
    )
    category = django_filters.NumberFilter(
        field_name="service__category",
        lookup_expr='exact'
    )

    class Meta:
        model = Subscription
        fields = ['start_date', 'end_date', 'category']
