from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal

from ..models import Status, TransactionType, Category, Subcategory, CashFlowRecord


class APITests(APITestCase):
    def setUp(self):
        """Создаем тестовые данные и клиент API"""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

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

        self.record_data = {
            'created_date': date.today().isoformat(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '1000.00',
            'comment': 'Тестовая запись через API'
        }

    def test_create_record(self):
        """Тест создания записи через API"""
        url = reverse('cashflowrecord-list')
        response = self.client.post(url, self.record_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CashFlowRecord.objects.count(), 1)
        self.assertEqual(CashFlowRecord.objects.get().comment, 'Тестовая запись через API')

    def test_get_records(self):
        """Тест получения списка записей через API"""
        # Создаем тестовую запись
        CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('1000.00'),
            comment="Тестовая запись"
        )

        url = reverse('cashflowrecord-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['comment'], 'Тестовая запись')

    def test_update_record(self):
        """Тест обновления записи через API"""
        record = CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('1000.00'),
            comment="Тестовая запись"
        )

        url = reverse('cashflowrecord-detail', args=[record.id])
        updated_data = self.record_data.copy()
        updated_data['comment'] = 'Обновленная запись'
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.comment, 'Обновленная запись')

    def test_delete_record(self):
        """Тест удаления записи через API"""
        record = CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('1000.00'),
            comment="Тестовая запись"
        )

        url = reverse('cashflowrecord-detail', args=[record.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CashFlowRecord.objects.count(), 0)

    def test_summary_endpoint(self):
        """Тест эндпоинта сводной статистики"""
        # Создаем тестовые записи
        CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('1000.00'),
            comment="Доход"
        )

        expense_type = TransactionType.objects.create(name="Списание")
        expense_category = Category.objects.create(
            transaction_type=expense_type,
            name="Расходы"
        )
        expense_subcategory = Subcategory.objects.create(
            category=expense_category,
            name="Прочие"
        )

        CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=expense_type,
            category=expense_category,
            subcategory=expense_subcategory,
            amount=Decimal('300.00'),
            comment="Расход"
        )

        url = reverse('cashflowrecord-summary')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expense', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '1000.00')
        self.assertEqual(response.data['total_expense'], '300.00')
        self.assertEqual(response.data['balance'], '700.00')