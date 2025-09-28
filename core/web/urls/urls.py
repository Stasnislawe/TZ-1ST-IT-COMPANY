from django.urls import path
from ..views import views

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
]