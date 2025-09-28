from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import CashFlowRecord, Status, TransactionType, Category, Subcategory
from ..forms import CashFlowRecordForm


class StatusListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка статусов.

    Использует общий шаблон dictionary_list.html для справочников.
    """
    model = Status
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статусы'
        context['model_name'] = 'status'
        return context


class TransactionTypeListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка типов операций.
    """
    model = TransactionType
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Типы операций'
        context['model_name'] = 'transactiontype'
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка категорий.
    """
    model = Category
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['model_name'] = 'category'
        return context


class SubcategoryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка подкатегорий.
    """
    model = Subcategory
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подкатегории'
        context['model_name'] = 'subcategory'
        return context


class CashFlowRecordListView(ListView):
    """
    Представление для отображения списка записей денежных потоков.

    Поддерживает пагинацию и фильтрацию по различным параметрам.
    """
    model = CashFlowRecord
    template_name = 'cash_flow/record_list.html'
    context_object_name = 'records'
    paginate_by = 20

    def get_queryset(self):
        """
         Возвращает оптимизированный queryset с применением фильтров.

         Поддерживает фильтрацию по:
         - статусу, типу операции, категории, подкатегории
         - периоду (дата от/до)
         """
        queryset = super().get_queryset().select_related(
            'status', 'transaction_type', 'category', 'subcategory'
        )

        # Получаем параметры фильтрации из GET-запроса
        status = self.request.GET.get('status')
        transaction_type = self.request.GET.get('transaction_type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        # Применяем фильтры
        if status:
            queryset = queryset.filter(status_id=status)
        if transaction_type:
            queryset = queryset.filter(transaction_type_id=transaction_type)
        if category:
            queryset = queryset.filter(category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            queryset = queryset.filter(created_date__gte=date_from)
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            queryset = queryset.filter(created_date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст данные для фильтров и текущие значения фильтров.
        """
        context = super().get_context_data(**kwargs)

        # Добавляем формы для фильтров
        context['statuses'] = Status.objects.all()
        context['transaction_types'] = TransactionType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        # Передаем текущие значения фильтров для сохранения в форме
        context['current_filters'] = {
            'status': self.request.GET.get('status', ''),
            'transaction_type': self.request.GET.get('transaction_type', ''),
            'category': self.request.GET.get('category', ''),
            'subcategory': self.request.GET.get('subcategory', ''),
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_to', ''),
        }

        return context


class CashFlowRecordCreateView(CreateView):
    """
    Представление для создания новой записи денежного потока.
    """
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'cash_flow/record_form.html'
    success_url = reverse_lazy('cash_flow:index')

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новой записи ДДС'
        return context


class CashFlowRecordUpdateView(UpdateView):
    """
    Представление для редактирования существующей записи денежного потока.
    """
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'cash_flow/record_form.html'
    success_url = reverse_lazy('cash_flow:index')

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование записи ДДС'
        return context


class CashFlowRecordDeleteView(DeleteView):
    """
    Представление для удаления записи денежного потока.
    """
    model = CashFlowRecord
    template_name = 'cash_flow/record_confirm_delete.html'
    success_url = reverse_lazy('cash_flow:index')

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно удалена!')
        return super().form_valid(form)


class DictionaryManageView(TemplateView):
    """
    Представление для управления справочниками системы.

    Отображает все справочники на одной странице для удобного управления.
    """
    template_name = 'cash_flow/dictionary_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['transaction_types'] = TransactionType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context


def load_categories(request):
    """AJAX загрузка категорий"""
    transaction_type_id = request.GET.get('transaction_type_id')
    if transaction_type_id:
        categories = Category.objects.filter(transaction_type_id=transaction_type_id)
        # Возвращаем только имя категории, без типа операции
        data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def load_subcategories(request):
    """AJAX загрузка подкатегорий"""
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id)
        # Возвращаем только имя подкатегории, без категории и типа операции
        data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)