from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Q, Count
from datetime import datetime, timedelta
from ..models import Status, TransactionType, Category, Subcategory, CashFlowRecord
from ..serializers import (
    StatusSerializer, TransactionTypeSerializer, CategorySerializer,
    SubcategorySerializer, CashFlowRecordSerializer, CashFlowRecordCreateSerializer,
    CashFlowRecordSummarySerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления статусами операций.

    Предоставляет CRUD операции для модели Status.
    Требует аутентификации пользователя.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class TransactionTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления типами транзакций.

    Предоставляет CRUD операции для модели TransactionType.
    Требует аутентификации пользователя.
    """
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления категориями операций.

    Предоставляет CRUD операции для модели Category.
    Поддерживает фильтрацию по типу транзакции.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['transaction_type']
    search_fields = ['name']
    ordering_fields = ['name', 'transaction_type__name']


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления подкатегориями операций.

    Предоставляет CRUD операции для модели Subcategory.
    Поддерживает фильтрацию по категории и типу транзакции.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'category__transaction_type']
    search_fields = ['name']
    ordering_fields = ['name', 'category__name']


class CashFlowRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления записями денежных потоков.

    Предоставляет полный CRUD для записей CashFlowRecord.
    Включает дополнительные действия для аналитики и отчетности.
    """
    queryset = CashFlowRecord.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'status', 'transaction_type', 'category', 'subcategory', 'created_date'
    ]
    search_fields = ['comment', 'category__name', 'subcategory__name']
    ordering_fields = ['created_date', 'amount']
    ordering = ['-created_date']

    def get_serializer_class(self):
        """
        Выбор сериализатора в зависимости от действия.

        Для создания и обновления используется CashFlowRecordCreateSerializer,
        для остальных действий - CashFlowRecordSerializer.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return CashFlowRecordCreateSerializer
        return CashFlowRecordSerializer

    def get_queryset(self):
        """
        Оптимизация queryset с select_related и фильтрация по датам.
        """
        queryset = super().get_queryset()

        # Фильтрация по дате (период)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(created_date__gte=date_from)
            except ValueError:
                pass

        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(created_date__lte=date_to)
            except ValueError:
                pass

        return queryset.select_related(
            'status', 'transaction_type', 'category', 'subcategory'
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Сводная статистика по доходам и расходам"""
        queryset = self.get_queryset()

        # Параметры периода
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        # Если период не указан, используем текущий месяц
        if not date_from or not date_to:
            today = datetime.now().date()
            date_from = today.replace(day=1)  # Первое число текущего месяца
            next_month = today.replace(day=28) + timedelta(days=4)  # Переход к следующему месяцу
            date_to = next_month - timedelta(days=next_month.day)  # Последний день текущего месяца

        # Сумма пополнений (доходов)
        income = queryset.filter(
            transaction_type__name='Пополнение',
            created_date__gte=date_from,
            created_date__lte=date_to
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Сумма списаний (расходов)
        expense = queryset.filter(
            transaction_type__name='Списание',
            created_date__gte=date_from,
            created_date__lte=date_to
        ).aggregate(total=Sum('amount'))['total'] or 0

        balance = income - expense

        data = {
            'total_income': income,
            'total_expense': expense,
            'balance': balance,
            'period_start': date_from,
            'period_end': date_to
        }

        serializer = CashFlowRecordSummarySerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Статистика по категориям"""
        queryset = self.get_queryset()

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        # Фильтрация по периоду
        if date_from and date_to:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(created_date__range=[date_from, date_to])
            except ValueError:
                pass

        # Группировка по категориям
        result = queryset.values(
            'category__id',
            'category__name',
            'transaction_type__name'
        ).annotate(
            total_amount=Sum('amount'),
            record_count=Count('id')
        ).order_by('transaction_type__name', '-total_amount')

        return Response(result)

    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """Ежемесячный отчет"""
        queryset = self.get_queryset()

        # Используем Django ORM функции для извлечения года и месяца
        result = queryset.annotate(
            year=ExtractYear('created_date'),
            month=ExtractMonth('created_date')
        ).values('year', 'month').annotate(
            income=Sum('amount', filter=Q(transaction_type__name='Пополнение')),
            expense=Sum('amount', filter=Q(transaction_type__name='Списание')),
            record_count=Count('id')
        ).order_by('-year', '-month')

        # Обрабатываем результаты
        formatted_result = []
        for item in result:
            formatted_item = {
                'year': int(item['year']),
                'month': int(item['month']),
                'period': f"{item['month']:02d}/{item['year']}",  # Исправленный формат
                'income': float(item['income'] or 0),
                'expense': float(item['expense'] or 0),
                'balance': float((item['income'] or 0) - (item['expense'] or 0)),
                'record_count': item['record_count']
            }
            formatted_result.append(formatted_item)

        return Response(formatted_result)


