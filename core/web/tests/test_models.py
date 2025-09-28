from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, datetime
from decimal import Decimal

from ..models import Status, TransactionType, Category, Subcategory, CashFlowRecord


class ModelTests(TestCase):
    def setUp(self):
        """Создаем тестовые данные"""
        self.status = Status.objects.create(name="Бизнес")
        self.transaction_type_income = TransactionType.objects.create(name="Пополнение")
        self.transaction_type_expense = TransactionType.objects.create(name="Списание")

        self.category_income = Category.objects.create(
            transaction_type=self.transaction_type_income,
            name="Зарплата"
        )
        self.category_expense = Category.objects.create(
            transaction_type=self.transaction_type_expense,
            name="Маркетинг"
        )

        self.subcategory_income = Subcategory.objects.create(
            category=self.category_income,
            name="Аванс"
        )
        self.subcategory_expense = Subcategory.objects.create(
            category=self.category_expense,
            name="Реклама"
        )

    def test_status_creation(self):
        """Тест создания статуса"""
        self.assertEqual(str(self.status), "Бизнес")
        self.assertEqual(Status.objects.count(), 1)

    def test_transaction_type_creation(self):
        """Тест создания типа операции"""
        self.assertEqual(str(self.transaction_type_income), "Пополнение")
        self.assertEqual(TransactionType.objects.count(), 2)

    def test_category_creation(self):
        """Тест создания категории"""
        self.assertEqual(str(self.category_income), "Пополнение - Зарплата")
        self.assertEqual(Category.objects.count(), 2)

        # Проверка связи с типом операции
        self.assertEqual(self.category_income.transaction_type, self.transaction_type_income)

    def test_subcategory_creation(self):
        """Тест создания подкатегории"""
        self.assertEqual(str(self.subcategory_income), "Пополнение - Зарплата - Аванс")
        self.assertEqual(Subcategory.objects.count(), 2)

        # Проверка связи с категорией
        self.assertEqual(self.subcategory_income.category, self.category_income)

    def test_cashflow_record_creation(self):
        """Тест создания записи ДДС"""
        record = CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type_income,
            category=self.category_income,
            subcategory=self.subcategory_income,
            amount=Decimal('1000.00'),
            comment="Тестовая запись"
        )

        self.assertEqual(record.amount, Decimal('1000.00'))
        self.assertEqual(record.comment, "Тестовая запись")
        self.assertEqual(record.transaction_type.name, "Пополнение")
        self.assertEqual(CashFlowRecord.objects.count(), 1)

    def test_cashflow_record_validation(self):
        """Тест валидации записи ДДС"""
        # Тест отрицательной суммы
        record = CashFlowRecord(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type_income,
            category=self.category_income,
            subcategory=self.subcategory_income,
            amount=Decimal('-100.00'),  # Отрицательная сумма
            comment="Невалидная запись"
        )

        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_automatic_date_field(self):
        """Тест автоматического заполнения даты"""
        record = CashFlowRecord.objects.create(
            status=self.status,
            transaction_type=self.transaction_type_income,
            category=self.category_income,
            subcategory=self.subcategory_income,
            amount=Decimal('500.00')
        )

        # Дата должна быть установлена автоматически
        self.assertIsNotNone(record.created_date)

        # Приводим к типу date
        if hasattr(record.created_date, 'date'):
            record_date = record.created_date.date()
        else:
            record_date = record.created_date

        # Сравниваем с текущей датой
        self.assertEqual(record_date, date.today())

    def test_logical_dependencies(self):
        """Тест логических зависимостей между сущностями"""
        # Создаем запись с неправильной связью категория-тип
        # Используем категорию от расходов с типом операций доходов
        record = CashFlowRecord(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type_income,  # Пополнение
            category=self.category_expense,  # Категория от Списания - ДОЛЖНА ВЫЗВАТЬ ОШИБКУ
            subcategory=self.subcategory_expense,
            amount=Decimal('100.00')
        )

        # Должна возникнуть ошибка валидации
        with self.assertRaises(ValidationError) as context:
            record.full_clean()

        # Проверяем, что ошибка содержит ожидаемое сообщение
        self.assertIn('category', context.exception.error_dict)

    def test_string_representations(self):
        """Тест строковых представлений моделей"""
        self.assertEqual(str(self.status), "Бизнес")
        self.assertEqual(str(self.transaction_type_income), "Пополнение")
        self.assertEqual(str(self.category_income), "Пополнение - Зарплата")
        self.assertEqual(str(self.subcategory_income), "Пополнение - Зарплата - Аванс")

        record = CashFlowRecord.objects.create(
            created_date=date(2025, 1, 1),
            status=self.status,
            transaction_type=self.transaction_type_income,
            category=self.category_income,
            subcategory=self.subcategory_income,
            amount=Decimal('1000.00')
        )

        self.assertIn("01.01.2025", str(record))
        self.assertIn("1000.00", str(record))