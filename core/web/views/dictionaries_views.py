from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from ..models import Status, TransactionType, Category, Subcategory
from ..forms import StatusForm, TransactionTypeForm, CategoryForm, SubcategoryForm


# Status Views
class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статусы'
        context['model_name'] = 'status'
        context['create_url'] = 'cash_flow:status_create'
        context['list_url'] = 'cash_flow:status_list'
        context['edit_url'] = 'cash_flow:status_edit'
        context['delete_url'] = 'cash_flow:status_delete'
        return context


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:status_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статусы'
        context['model_name'] = 'status'
        context['create_url'] = 'cash_flow:status_create'
        context['list_url'] = 'cash_flow:status_list'
        context['edit_url'] = 'cash_flow:status_edit'
        context['delete_url'] = 'cash_flow:status_delete'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан!')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:status_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статусы'
        context['model_name'] = 'status'
        context['create_url'] = 'cash_flow:status_create'
        context['list_url'] = 'cash_flow:status_list'
        context['edit_url'] = 'cash_flow:status_edit'
        context['delete_url'] = 'cash_flow:status_delete'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен!')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'cash_flow/dictionary_confirm_delete.html'
    success_url = reverse_lazy('cash_flow:status_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статусы'
        context['model_name'] = 'status'
        context['create_url'] = 'cash_flow:status_create'
        context['list_url'] = 'cash_flow:status_list'
        context['edit_url'] = 'cash_flow:status_edit'
        context['delete_url'] = 'cash_flow:status_delete'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Статус успешно удален!')
        return super().delete(request, *args, **kwargs)


# TransactionType Views
class TransactionTypeListView(LoginRequiredMixin, ListView):
    model = TransactionType
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Типы операций'
        context['model_name'] = 'transactiontype'
        context['create_url'] = 'cash_flow:transaction_type_create'
        context['list_url'] = 'cash_flow:transaction_type_list'
        context['edit_url'] = 'cash_flow:transaction_type_edit'
        context['delete_url'] = 'cash_flow:transaction_type_delete'
        return context


class TransactionTypeCreateView(LoginRequiredMixin, CreateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:transaction_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Типы операций'
        context['model_name'] = 'transactiontype'
        context['create_url'] = 'cash_flow:transaction_type_create'
        context['list_url'] = 'cash_flow:transaction_type_list'
        context['edit_url'] = 'cash_flow:transaction_type_edit'
        context['delete_url'] = 'cash_flow:transaction_type_delete'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Тип операции успешно создан!')
        return super().form_valid(form)


class TransactionTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:transaction_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Типы операций'
        context['model_name'] = 'transactiontype'
        context['create_url'] = 'cash_flow:transaction_type_create'
        context['list_url'] = 'cash_flow:transaction_type_list'
        context['edit_url'] = 'cash_flow:transaction_type_edit'
        context['delete_url'] = 'cash_flow:transaction_type_delete'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Тип операции успешно обновлен!')
        return super().form_valid(form)


class TransactionTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TransactionType
    template_name = 'cash_flow/dictionary_confirm_delete.html'
    success_url = reverse_lazy('cash_flow:transaction_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Типы операций'
        context['model_name'] = 'transactiontype'
        context['create_url'] = 'cash_flow:transaction_type_create'
        context['list_url'] = 'cash_flow:transaction_type_list'
        context['edit_url'] = 'cash_flow:transaction_type_edit'
        context['delete_url'] = 'cash_flow:transaction_type_delete'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Тип операции успешно удален!')
        return super().delete(request, *args, **kwargs)


# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['model_name'] = 'category'
        context['create_url'] = 'cash_flow:category_create'
        context['list_url'] = 'cash_flow:category_list'
        context['edit_url'] = 'cash_flow:category_edit'
        context['delete_url'] = 'cash_flow:category_delete'
        context['transaction_types'] = TransactionType.objects.all()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['model_name'] = 'category'
        context['create_url'] = 'cash_flow:category_create'
        context['list_url'] = 'cash_flow:category_list'
        context['edit_url'] = 'cash_flow:category_edit'
        context['delete_url'] = 'cash_flow:category_delete'
        context['transaction_types'] = TransactionType.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['model_name'] = 'category'
        context['create_url'] = 'cash_flow:category_create'
        context['list_url'] = 'cash_flow:category_list'
        context['edit_url'] = 'cash_flow:category_edit'
        context['delete_url'] = 'cash_flow:category_delete'
        context['transaction_types'] = TransactionType.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'cash_flow/dictionary_confirm_delete.html'
    success_url = reverse_lazy('cash_flow:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['model_name'] = 'category'
        context['create_url'] = 'cash_flow:category_create'
        context['list_url'] = 'cash_flow:category_list'
        context['edit_url'] = 'cash_flow:category_edit'
        context['delete_url'] = 'cash_flow:category_delete'
        context['transaction_types'] = TransactionType.objects.all()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Категория успешно удалена!')
        return super().delete(request, *args, **kwargs)


# Subcategory Views
class SubcategoryListView(LoginRequiredMixin, ListView):
    model = Subcategory
    template_name = 'cash_flow/dictionary_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подкатегории'
        context['model_name'] = 'subcategory'
        context['create_url'] = 'cash_flow:subcategory_create'
        context['list_url'] = 'cash_flow:subcategory_list'
        context['edit_url'] = 'cash_flow:subcategory_edit'
        context['delete_url'] = 'cash_flow:subcategory_delete'
        context['categories'] = Category.objects.select_related('transaction_type').all()
        return context


class SubcategoryCreateView(LoginRequiredMixin, CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:subcategory_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подкатегории'
        context['model_name'] = 'subcategory'
        context['create_url'] = 'cash_flow:subcategory_create'
        context['list_url'] = 'cash_flow:subcategory_list'
        context['edit_url'] = 'cash_flow:subcategory_edit'
        context['delete_url'] = 'cash_flow:subcategory_delete'
        context['categories'] = Category.objects.select_related('transaction_type').all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно создана!')
        return super().form_valid(form)


class SubcategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cash_flow/dictionary_form.html'
    success_url = reverse_lazy('cash_flow:subcategory_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подкатегории'
        context['model_name'] = 'subcategory'
        context['create_url'] = 'cash_flow:subcategory_create'
        context['list_url'] = 'cash_flow:subcategory_list'
        context['edit_url'] = 'cash_flow:subcategory_edit'
        context['delete_url'] = 'cash_flow:subcategory_delete'
        context['categories'] = Category.objects.select_related('transaction_type').all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно обновлена!')
        return super().form_valid(form)


class SubcategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Subcategory
    template_name = 'cash_flow/dictionary_confirm_delete.html'
    success_url = reverse_lazy('cash_flow:subcategory_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подкатегории'
        context['model_name'] = 'subcategory'
        context['create_url'] = 'cash_flow:subcategory_create'
        context['list_url'] = 'cash_flow:subcategory_list'
        context['edit_url'] = 'cash_flow:subcategory_edit'
        context['delete_url'] = 'cash_flow:subcategory_delete'
        context['categories'] = Category.objects.select_related('transaction_type').all()
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Подкатегория успешно удалена!')
        return super().delete(request, *args, **kwargs)