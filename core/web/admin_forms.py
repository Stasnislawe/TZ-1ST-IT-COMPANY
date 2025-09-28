from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from .models import CashFlowRecord, Category, Subcategory


class CashFlowRecordAdminForm(forms.ModelForm):
    """Форма для админки с динамической загрузкой категорий"""

    class Meta:
        model = CashFlowRecord
        fields = '__all__'
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Статус не обязательный
        self.fields['status'].required = False

        # Для новых записей - пустые queryset, будут заполняться через JS
        if not self.instance.pk:
            self.fields['category'].queryset = Category.objects.none()
            self.fields['subcategory'].queryset = Subcategory.objects.none()
        else:
            # Для существующих записей - ограничиваем по выбранному типу
            if self.instance.transaction_type:
                self.fields['category'].queryset = Category.objects.filter(
                    transaction_type=self.instance.transaction_type
                )
            if self.instance.category:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category=self.instance.category
                )

    def clean_amount(self):
        """Валидация суммы"""
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise ValidationError('Сумма обязательна для заполнения')

        if isinstance(amount, str):
            try:
                clean_amount = amount.replace(' ', '').replace(',', '.')
                amount = Decimal(clean_amount)
            except (ValueError, InvalidOperation):
                raise ValidationError('Введите корректную сумму')

        if amount <= 0:
            raise ValidationError('Сумма должна быть положительным числом')

        return amount

    def clean(self):
        """Валидация согласованности категорий и подкатегорий"""
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                raise ValidationError({
                    'category': 'Выбранная категория не принадлежит выбранному типу операции.'
                })

        if subcategory and category:
            if subcategory.category != category:
                raise ValidationError({
                    'subcategory': 'Выбранная подкатегория не принадлежит выбранной категории.'
                })

        return cleaned_data