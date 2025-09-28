from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal

from ..forms import CashFlowRecordForm
from ..models import Status, TransactionType, Category, Subcategory, CashFlowRecord


class FormTests(TestCase):
    def setUp(self):
        """Создаем тестовые данные"""
        self.status = Status.objects.create(name="Бизнес")
        self.transaction_type = TransactionType.objects.create(name="Пополнение")
        self.category = Category.objects.create(
            transaction_type=self.transaction_type,
            name="Зарплата"
        )
        self.subcategory = Subcategory.objects.create(
            category=self.category,
            name="Аванс"
        )

    def test_valid_form(self):
        """Тест валидной формы"""
        form_data = {
            'created_date': date.today(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '1500.00',
            'comment': 'Тестовый комментарий'
        }
        form = CashFlowRecordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_fields(self):
        """Тест формы с отсутствующими обязательными полями"""
        form_data = {
            'created_date': date.today(),
            'status': self.status.id,
            # Пропущены transaction_type, category, subcategory, amount
        }
        form = CashFlowRecordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('transaction_type', form.errors)
        self.assertIn('category', form.errors)
        self.assertIn('subcategory', form.errors)
        self.assertIn('amount', form.errors)

    def test_invalid_amount(self):
        """Тест невалидной суммы"""
        form_data = {
            'created_date': date.today(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '-100.00',  # Отрицательная сумма
            'comment': 'Тестовый комментарий'
        }
        form = CashFlowRecordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_form_saves_correctly(self):
        """Тест сохранения формы"""
        form_data = {
            'created_date': date.today(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '2000.00',
            'comment': 'Тест сохранения'
        }
        form = CashFlowRecordForm(data=form_data)
        self.assertTrue(form.is_valid())

        record = form.save()
        self.assertEqual(record.amount, Decimal('2000.00'))
        self.assertEqual(record.comment, 'Тест сохранения')
        self.assertEqual(CashFlowRecord.objects.count(), 1)

    def test_status_field_not_required(self):
        """Тест что поле статус необязательное"""
        form_data = {
            'created_date': date.today(),
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '2000.00',
            # status пропущен - должен быть валидным
        }
        form = CashFlowRecordForm(data=form_data)
        self.assertTrue(form.is_valid())