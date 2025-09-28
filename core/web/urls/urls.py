from django.urls import path
from ..views import views
from ..views.dictionaries_views import (
    StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView,
    TransactionTypeListView, TransactionTypeCreateView, TransactionTypeUpdateView, TransactionTypeDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    SubcategoryListView, SubcategoryCreateView, SubcategoryUpdateView, SubcategoryDeleteView,
)


app_name = 'cash_flow'

urlpatterns = [
    # Основные страницы
    path('', views.CashFlowRecordListView.as_view(), name='index'),
    path('records/create/', views.CashFlowRecordCreateView.as_view(), name='record_create'),
    path('records/<int:pk>/edit/', views.CashFlowRecordUpdateView.as_view(), name='record_edit'),
    path('records/<int:pk>/delete/', views.CashFlowRecordDeleteView.as_view(), name='record_delete'),

    # Справочники
    path('dictionaries/', views.DictionaryManageView.as_view(), name='dictionary_manage'),
    path('dictionaries/status/', views.StatusListView.as_view(), name='status_list'),
    path('dictionaries/transaction-type/', views.TransactionTypeListView.as_view(), name='transactiontype_list'),
    path('dictionaries/category/', views.CategoryListView.as_view(), name='category_list'),
    path('dictionaries/subcategory/', views.SubcategoryListView.as_view(), name='subcategory_list'),

    # AJAX endpoints
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),

    # Status URLs
    path('statuses/', StatusListView.as_view(), name='status_list'),
    path('statuses/create/', StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/edit/', StatusUpdateView.as_view(), name='status_edit'),
    path('statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),

    # TransactionType URLs
    path('transaction-types/', TransactionTypeListView.as_view(), name='transaction_type_list'),
    path('transaction-types/create/', TransactionTypeCreateView.as_view(), name='transaction_type_create'),
    path('transaction-types/<int:pk>/edit/', TransactionTypeUpdateView.as_view(), name='transaction_type_edit'),
    path('transaction-types/<int:pk>/delete/', TransactionTypeDeleteView.as_view(), name='transaction_type_delete'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Subcategory URLs
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory_list'),
    path('subcategories/create/', SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategories/<int:pk>/edit/', SubcategoryUpdateView.as_view(), name='subcategory_edit'),
    path('subcategories/<int:pk>/delete/', SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]