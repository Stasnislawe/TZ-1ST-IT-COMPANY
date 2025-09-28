from rest_framework import serializers
from .models import Status, TransactionType, Category, Subcategory, CashFlowRecord


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор для статуса"""
    class Meta:
        model = Status
        fields = ['id', 'name']
        read_only_fields = ['id']


class TransactionTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для типа транзакции"""
    class Meta:
        model = TransactionType
        fields = ['id', 'name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'transaction_type', 'transaction_type_name']
        read_only_fields = ['id']


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    transaction_type_name = serializers.CharField(source='category.transaction_type.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_name', 'transaction_type_name']
        read_only_fields = ['id']


class CashFlowRecordSerializer(serializers.ModelSerializer):
    """Сериализатор для ДДС"""
    status_name = serializers.CharField(source='status.name', read_only=True)
    transaction_type_name = serializers.CharField(source='transaction_type.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)

    class Meta:
        model = CashFlowRecord
        fields = [
            'id', 'created_date', 'status', 'status_name',
            'transaction_type', 'transaction_type_name',
            'category', 'category_name', 'subcategory', 'subcategory_name',
            'amount', 'comment'
        ]
        read_only_fields = ['id']


class CashFlowRecordCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания записи ДДС"""
    class Meta:
        model = CashFlowRecord
        fields = [
            'created_date', 'status', 'transaction_type',
            'category', 'subcategory', 'amount', 'comment'
        ]

    def validate(self, data):
        """
        Валидация логических зависимостей
        """
        # Проверка соответствия категории и типа операции
        if 'category' in data and 'transaction_type' in data:
            if data['category'].transaction_type != data['transaction_type']:
                raise serializers.ValidationError({
                    'category': 'Выбранная категория не принадлежит выбранному типу операции'
                })

        # Проверка соответствия подкатегории и категории
        if 'subcategory' in data and 'category' in data:
            if data['subcategory'].category != data['category']:
                raise serializers.ValidationError({
                    'subcategory': 'Выбранная подкатегория не принадлежит выбранной категории'
                })

        # Проверка суммы
        if 'amount' in data and data['amount'] <= 0:
            raise serializers.ValidationError({
                'amount': 'Сумма должна быть положительным числом'
            })

        return data


class CashFlowRecordSummarySerializer(serializers.Serializer):
    """Сериализатор для сводной статистики"""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    period_start = serializers.DateField()
    period_end = serializers.DateField()

    class Meta:
        fields = ['total_income', 'total_expense', 'balance', 'period_start', 'period_end']