from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views.api_views import (
    StatusViewSet, TransactionTypeViewSet, CategoryViewSet,
    SubcategoryViewSet, CashFlowRecordViewSet
)

# Создаем основной роутер для API
router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'transaction-types', TransactionTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'records', CashFlowRecordViewSet)

# URL-паттерны API
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # Для браузерного API (аутентификация)
]
