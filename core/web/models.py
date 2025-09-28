from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Status(models.Model):
    """
    Модель для статусов записей ДДС.
    Содержит предустановленные значения: Бизнес, Личное, Налог.
    Список может расширяться через админку.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название статуса"
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    """
    Модель для типов операций ДДС.
    Содержит предустановленные значения: Пополнение, Списание.
    Список может расширяться через админку.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тип операции"
    )

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель для категорий ДДС.
    Примеры: Инфраструктура, Маркетинг.
    Каждая категория привязана к определенному типу операции.
    """
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Тип операции"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['transaction_type', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['transaction_type', 'name'],
                name='unique_category_per_type'
            )
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.name}"


class Subcategory(models.Model):
    """
    Модель для подкатегорий ДДС.
    Связана с категорией через ForeignKey.
    Примеры: для категории "Инфраструктура" - "VPS", "Proxy"
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Категория"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название подкатегории"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['category', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                name='unique_subcategory_per_category'
            )
        ]

    def __str__(self):
        return f"{self.category} - {self.name}"


class CashFlowRecord(models.Model):
    """
    Основная модель для записей о движении денежных средств (ДДС).
    Содержит все необходимые поля согласно техническому заданию.
    """
    created_date = models.DateField(
        default=timezone.now,
        verbose_name="Дата создания записи",
        help_text="Заполняется автоматически, но может быть изменена вручную"
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        blank=True,
        null=True,
        default=None
    )

    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        verbose_name="Тип операции"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Сумма",
        help_text="Количество средств в рублях"
    )

    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий",
        help_text="Комментарий к записи в свободной форме (необязательное поле)"
    )

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['created_date']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['category', 'subcategory']),
        ]

    def clean(self):
        """
        Валидация целостности данных согласно бизнес-правилам
        """
        errors = {}

        # Проверка обязательных полей
        if not self.amount or self.amount <= 0:
            errors['amount'] = 'Сумма должна быть положительным числом'

        if not self.transaction_type_id:
            errors['transaction_type'] = 'Тип операции обязателен для заполнения'

        if not self.category_id:
            errors['category'] = 'Категория обязательна для заполнения'
        elif self.transaction_type_id and self.category.transaction_type_id != self.transaction_type_id:
            errors['category'] = 'Выбранная категория не принадлежит выбранному типу операции'

        if not self.subcategory_id:
            errors['subcategory'] = 'Подкатегория обязательна для заполнения'
        elif self.category_id and self.subcategory.category_id != self.category_id:
            errors['subcategory'] = 'Выбранная подкатегория не принадлежит выбранной категории'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической валидации
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ДДС #{self.id} - {self.created_date.strftime('%d.%m.%Y')} - {self.amount} руб."
