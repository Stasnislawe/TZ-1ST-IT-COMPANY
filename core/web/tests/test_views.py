from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal

from ..models import Status, TransactionType, Category, Subcategory, CashFlowRecord


class ViewTests(TestCase):
    def setUp(self):
        """Создаем тестовые данные и клиент"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Создаем тестовые данные
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

        # Создаем тестовые записи
        self.record = CashFlowRecord.objects.create(
            created_date=date.today(),
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('1000.00'),
            comment="Тестовая запись"
        )

        # Запись за вчера для тестирования фильтрации
        self.old_record = CashFlowRecord.objects.create(
            created_date=date.today() - timedelta(days=1),
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal('500.00'),
            comment="Старая запись"
        )

    def test_index_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('cash_flow:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash_flow/record_list.html')
        self.assertContains(response, "Тестовая запись")

    def test_index_view_with_filters(self):
        """Тест главной страницы с фильтрами"""
        # Фильтр по дате (только сегодняшние записи)
        response = self.client.get(reverse('cash_flow:index'), {
            'date_from': date.today().isoformat(),
            'date_to': date.today().isoformat()
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовая запись")
        self.assertNotContains(response, "Старая запись")

    def test_record_create_view_get(self):
        """Тест страницы создания записи (GET)"""
        response = self.client.get(reverse('cash_flow:record_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash_flow/record_form.html')

    def test_record_create_view_post(self):
        """Тест создания записи (POST)"""
        form_data = {
            'created_date': date.today().isoformat(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '2000.00',
            'comment': 'Новая тестовая запись'
        }
        response = self.client.post(reverse('cash_flow:record_create'), form_data)

        # Должен произойти редирект на главную страницу
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cash_flow:index'))

        # Проверяем что запись создана
        self.assertEqual(CashFlowRecord.objects.count(), 3)
        new_record = CashFlowRecord.objects.latest('id')
        self.assertEqual(new_record.amount, Decimal('2000.00'))
        self.assertEqual(new_record.comment, 'Новая тестовая запись')

    def test_record_edit_view(self):
        """Тест редактирования записи"""
        response = self.client.get(reverse('cash_flow:record_edit', args=[self.record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash_flow/record_form.html')

        # Тест POST запроса на редактирование
        form_data = {
            'created_date': self.record.created_date.isoformat(),
            'status': self.status.id,
            'transaction_type': self.transaction_type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '3000.00',  # Измененная сумма
            'comment': 'Обновленная запись'
        }
        response = self.client.post(reverse('cash_flow:record_edit', args=[self.record.id]), form_data)

        self.assertEqual(response.status_code, 302)
        self.record.refresh_from_db()
        self.assertEqual(self.record.amount, Decimal('3000.00'))
        self.assertEqual(self.record.comment, 'Обновленная запись')

    def test_record_delete_view(self):
        """Тест удаления записи"""
        # Тест GET запроса на подтверждение удаления
        response = self.client.get(reverse('cash_flow:record_delete', args=[self.record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash_flow/record_confirm_delete.html')

        # Тест POST запроса на удаление
        response = self.client.post(reverse('cash_flow:record_delete', args=[self.record.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cash_flow:index'))
        self.assertEqual(CashFlowRecord.objects.count(), 1)  # Осталась только старая запись

    def test_dictionary_manage_view(self):
        """Тест страницы управления справочниками"""
        response = self.client.get(reverse('cash_flow:dictionary_manage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash_flow/dictionary_manage.html')
        self.assertContains(response, "Статусы")
        self.assertContains(response, "Типы операций")

    def test_ajax_load_categories(self):
        """Тест AJAX загрузки категорий"""
        response = self.client.get(reverse('cash_flow:ajax_load_categories'), {
            'transaction_type_id': self.transaction_type.id
        })
        self.assertEqual(response.status_code, 200)

        # Ожидаем только имя категории, без типа операции
        expected_data = [{'id': self.category.id, 'name': self.category.name}]
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_data
        )

    def test_ajax_load_subcategories(self):
        """Тест AJAX загрузки подкатегорий"""
        response = self.client.get(reverse('cash_flow:ajax_load_subcategories'), {
            'category_id': self.category.id
        })
        self.assertEqual(response.status_code, 200)

        # Ожидаем только имя подкатегории, без категории и типа операции
        expected_data = [{'id': self.subcategory.id, 'name': self.subcategory.name}]
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_data
        )