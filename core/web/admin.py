from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Status, TransactionType, Category, Subcategory, CashFlowRecord
from .admin_forms import CashFlowRecordAdminForm


class AmountRangeFilter(admin.SimpleListFilter):
    """Кастомный фильтр для суммы"""
    title = 'Диапазон суммы'
    parameter_name = 'amount_range'

    def lookups(self, request, model_admin):
        return (
            ('0-1000', 'До 1,000 руб.'),
            ('1000-5000', '1,000 - 5,000 руб.'),
            ('5000-10000', '5,000 - 10,000 руб.'),
            ('10000+', 'Более 10,000 руб.'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-1000':
            return queryset.filter(amount__lte=1000)
        if self.value() == '1000-5000':
            return queryset.filter(amount__gt=1000, amount__lte=5000)
        if self.value() == '5000-10000':
            return queryset.filter(amount__gt=5000, amount__lte=10000)
        if self.value() == '10000+':
            return queryset.filter(amount__gt=10000)
        return queryset


@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    """Админка для записей ДДС"""
    form = CashFlowRecordAdminForm
    list_display = (
        'created_date',
        'status',
        'transaction_type',
        'category',
        'subcategory',
        'amount',
        'comment_preview'
    )
    list_filter = (
        'status',
        'transaction_type',
        'category',
        'subcategory',
        'created_date',
        AmountRangeFilter,
    )
    search_fields = (
        'comment',
        'category__name',
        'subcategory__name',
        'amount',
    )
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)
    list_per_page = 50

    fieldsets = (
        ('Основная информация', {
            'fields': ('created_date', 'status', 'transaction_type')
        }),
        ('Категоризация', {
            'fields': ('category', 'subcategory')
        }),
        ('Финансовые данные', {
            'fields': ('amount', 'comment')
        }),
    )

    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return '-'

    comment_preview.short_description = 'Комментарий (превью)'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return []

    def get_urls(self):
        """Добавляем AJAX URL для админки"""
        urls = super().get_urls()
        custom_urls = [
            path('ajax/load-all-categories/', self.admin_site.admin_view(self.load_all_categories),
                 name='cash_flow_load_all_categories'),
        ]
        return custom_urls + urls

    def load_all_categories(self, request):
        """Загрузка всех категорий и подкатегорий для клиентской фильтрации"""
        categories = Category.objects.all().values('id', 'name', 'transaction_type_id')
        subcategories = Subcategory.objects.all().values('id', 'name', 'category_id')

        data = {
            'categories': list(categories),
            'subcategories': list(subcategories),
        }
        return JsonResponse(data)

    class Media:
        js = (
            'admin/js/jquery.init.js',
            'js/cashflow_admin.js',
        )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """Добавляем URLs в контекст шаблона"""
        extra_context = extra_context or {}
        # Получаем базовый URL для AJAX запросов
        extra_context['ajax_load_categories_url'] = '/ajax/load-categories/'
        extra_context['ajax_load_subcategories_url'] = '/ajax/load-subcategories/'
        return super().changeform_view(request, object_id, form_url, extra_context)


# Регистрация остальных моделей остается без изменений
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'cashflow_records_count')
    search_fields = ('name',)
    ordering = ('name',)

    def cashflow_records_count(self, obj):
        return obj.cashflowrecord_set.count()

    cashflow_records_count.short_description = 'Количество записей'


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories_count', 'cashflow_records_count')
    search_fields = ('name',)
    ordering = ('name',)

    def categories_count(self, obj):
        return obj.categories.count()

    categories_count.short_description = 'Количество категорий'

    def cashflow_records_count(self, obj):
        return obj.cashflowrecord_set.count()

    cashflow_records_count.short_description = 'Количество записей'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transaction_type', 'subcategories_count', 'cashflow_records_count')
    list_filter = ('transaction_type',)
    search_fields = ('name', 'transaction_type__name')
    ordering = ('transaction_type', 'name')

    def subcategories_count(self, obj):
        return obj.subcategories.count()

    subcategories_count.short_description = 'Количество подкатегорий'

    def cashflow_records_count(self, obj):
        return obj.cashflowrecord_set.count()

    cashflow_records_count.short_description = 'Количество записей'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'transaction_type', 'cashflow_records_count')
    list_filter = ('category__transaction_type', 'category')
    search_fields = ('name', 'category__name')
    ordering = ('category', 'name')

    def transaction_type(self, obj):
        return obj.category.transaction_type

    transaction_type.short_description = 'Тип операции'

    def cashflow_records_count(self, obj):
        return obj.cashflowrecord_set.count()

    cashflow_records_count.short_description = 'Количество записей'


# Кастомизация заголовка админки
admin.site.site_header = 'Система управления движением денежных средств (ДДС)'
admin.site.site_title = 'ДДС Админка'
admin.site.index_title = 'Панель управления ДДС'