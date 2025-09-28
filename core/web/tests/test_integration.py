from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal

from ..models import Status, TransactionType, Category, Subcategory, CashFlowRecord


class IntegrationTests(TestCase):
    def setUp(self):
        """Создаем тестовые данные"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

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

    def test_complete_workflow(self):
        """Тест полного рабочего процесса: создание → редактирование → удаление"""
        # 1. Создание записи
        form_data = {
            'created_date': date.today().isoformat(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '1000.00',
            'comment': 'Тестовая запись'
        }

        response = self.client.post(reverse('cash_flow:record_create'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CashFlowRecord.objects.count(), 1)

        record = CashFlowRecord.objects.first()
        self.assertEqual(record.amount, Decimal('1000.00'))

        # 2. Редактирование записи
        form_data['amount'] = '2000.00'
        form_data['comment'] = 'Обновленная запись'

        response = self.client.post(reverse('cash_flow:record_edit', args=[record.id]), form_data)
        self.assertEqual(response.status_code, 302)

        record.refresh_from_db()
        self.assertEqual(record.amount, Decimal('2000.00'))
        self.assertEqual(record.comment, 'Обновленная запись')

        # 3. Удаление записи
        response = self.client.post(reverse('cash_flow:record_delete', args=[record.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CashFlowRecord.objects.count(), 0)

    def test_filter_workflow(self):
        """Тест рабочего процесса с фильтрацией"""
        # Создаем несколько записей
        for i in range(3):
            CashFlowRecord.objects.create(
                created_date=date(2025, 1, i + 1),
                status=self.status,
                transaction_type=self.transaction_type,
                category=self.category,
                subcategory=self.subcategory,
                amount=Decimal(f'{100 * (i + 1)}.00'),
                comment=f"Запись {i + 1}"
            )

        # Фильтруем записи за определенный период
        response = self.client.get(reverse('cash_flow:index'), {
            'date_from': '2025-01-02',
            'date_to': '2025-01-03'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Запись 2")
        self.assertContains(response, "Запись 3")
        self.assertNotContains(response, "Запись 1")