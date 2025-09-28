from decimal import InvalidOperation, Decimal
from django import forms
from django.core.exceptions import ValidationError

from .models import Subcategory, Category, CashFlowRecord, Status, TransactionType


class CashFlowRecordForm(forms.ModelForm):
    """Форма записи ДДС"""
    class Meta:
        model = CashFlowRecord
        fields = '__all__'
        widgets = {
            'created_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Статус не обязательный
        self.fields['status'].required = False

        # Для существующей записи - ограничиваем выбор категорий и подкатегорий
        if self.instance and self.instance.pk:
            # Устанавливаем правильные queryset для существующей записи
            if self.instance.transaction_type:
                # Получаем категории для текущего типа операции
                categories = Category.objects.filter(
                    transaction_type=self.instance.transaction_type
                )
                # Добавляем текущую категорию, если она не входит в queryset
                if self.instance.category and self.instance.category not in categories:
                    categories = categories | Category.objects.filter(id=self.instance.category.id)
                self.fields['category'].queryset = categories
            else:
                self.fields['category'].queryset = Category.objects.all()

            if self.instance.category:
                # Получаем подкатегории для текущей категории
                subcategories = Subcategory.objects.filter(
                    category=self.instance.category
                )
                # Добавляем текущую подкатегорию, если она не входит в queryset
                if self.instance.subcategory and self.instance.subcategory not in subcategories:
                    subcategories = subcategories | Subcategory.objects.filter(id=self.instance.subcategory.id)
                self.fields['subcategory'].queryset = subcategories
            else:
                self.fields['subcategory'].queryset = Subcategory.objects.all()
        else:
            # Для новой записи - все категории доступны
            self.fields['category'].queryset = Category.objects.all()
            self.fields['subcategory'].queryset = Subcategory.objects.all()

        # Устанавливаем начальные значения для существующей записи
        if self.instance and self.instance.pk:
            self.fields['created_date'].initial = self.instance.created_date
            if self.instance.status:
                self.fields['status'].initial = self.instance.status
            self.fields['transaction_type'].initial = self.instance.transaction_type
            self.fields['category'].initial = self.instance.category
            self.fields['subcategory'].initial = self.instance.subcategory
            self.fields['amount'].initial = self.instance.amount
            self.fields['comment'].initial = self.instance.comment

    def clean_amount(self):
        """Простая валидация суммы"""
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise ValidationError('Сумма обязательна для заполнения')

        # Если это строка, конвертируем в Decimal
        if isinstance(amount, str):
            try:
                # Убираем пробелы и заменяем запятую на точку
                clean_amount = amount.replace(' ', '').replace(',', '.')
                amount = Decimal(clean_amount)
            except (ValueError, InvalidOperation):
                raise ValidationError('Введите корректную сумму')

        if amount <= 0:
            raise ValidationError('Сумма должна быть положительным числом')

        return amount


# Формы для справочников
class StatusForm(forms.ModelForm):
    """Форма статуса"""
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TransactionTypeForm(forms.ModelForm):
    """Форма типа транзакции"""
    class Meta:
        model = TransactionType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    """Форма категории"""
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
        }


class SubcategoryForm(forms.ModelForm):
    """Форма подкатегории"""
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Для существующей записи ограничиваем выбор категорий
        if self.instance and self.instance.pk and self.instance.category:
            self.fields['category'].queryset = Category.objects.filter(
                transaction_type=self.instance.category.transaction_type
            )
