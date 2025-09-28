import django_filters
from .models import CashFlowRecord


class CashFlowRecordFilter(django_filters.FilterSet):
    """Фильтрация записей ДДС"""
    date_range = django_filters.DateFromToRangeFilter(field_name='created_date')
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = CashFlowRecord
        fields = {
            'status': ['exact'],
            'transaction_type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
            'created_date': ['gte', 'lte', 'exact'],
            'amount': ['gte', 'lte', 'exact'],
        }