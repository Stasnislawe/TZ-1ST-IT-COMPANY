(function($) {
    'use strict';

    // Функция для фильтрации категорий
    function filterCategories(transactionTypeId) {
        console.log('Filtering categories for transaction type:', transactionTypeId);
        var categorySelect = $('#id_category');
        var allCategories = categorySelect.data('all-categories') || [];
        var currentCategoryId = categorySelect.val();

        categorySelect.empty();
        categorySelect.append($('<option>').text('---------').attr('value', ''));

        if (transactionTypeId) {
            var filteredCategories = allCategories.filter(function(cat) {
                return cat.transaction_type_id == transactionTypeId;
            });

            console.log('Filtered categories:', filteredCategories);

            $.each(filteredCategories, function(index, category) {
                var option = $('<option>')
                    .text(category.name)
                    .attr('value', category.id);
                categorySelect.append(option);
            });

            // Восстанавливаем выбранное значение, если оно есть в отфильтрованных категориях
            if (currentCategoryId) {
                var exists = filteredCategories.some(function(cat) {
                    return cat.id == currentCategoryId;
                });
                if (exists) {
                    categorySelect.val(currentCategoryId);
                }
            }
        }

        // Обновляем подкатегории
        filterSubcategories(categorySelect.val());
    }

    // Функция для фильтрации подкатегорий
    function filterSubcategories(categoryId) {
        console.log('Filtering subcategories for category:', categoryId);
        var subcategorySelect = $('#id_subcategory');
        var allSubcategories = subcategorySelect.data('all-subcategories') || [];
        var currentSubcategoryId = subcategorySelect.val();

        subcategorySelect.empty();
        subcategorySelect.append($('<option>').text('---------').attr('value', ''));

        if (categoryId) {
            var filteredSubcategories = allSubcategories.filter(function(sub) {
                return sub.category_id == categoryId;
            });

            console.log('Filtered subcategories:', filteredSubcategories);

            $.each(filteredSubcategories, function(index, subcategory) {
                var option = $('<option>')
                    .text(subcategory.name)
                    .attr('value', subcategory.id);
                subcategorySelect.append(option);
            });

            // Восстанавливаем выбранное значение
            if (currentSubcategoryId) {
                var exists = filteredSubcategories.some(function(sub) {
                    return sub.id == currentSubcategoryId;
                });
                if (exists) {
                    subcategorySelect.val(currentSubcategoryId);
                }
            }
        }
    }

    // Инициализация при загрузке страницы
    $(document).ready(function() {
        console.log('CashFlow Admin JS loaded');

        // Загружаем все категории и подкатегории
        $.ajax({
            url: '/admin/cash_flow/cashflowrecord/ajax/load-all-categories/',
            success: function(data) {
                console.log('Loaded categories data:', data);
                $('#id_category').data('all-categories', data.categories);
                $('#id_subcategory').data('all-subcategories', data.subcategories);

                // Инициализируем фильтрацию на основе текущих значений
                var transactionTypeId = $('#id_transaction_type').val();
                var categoryId = $('#id_category').val();

                console.log('Initial values - transactionType:', transactionTypeId, 'category:', categoryId);

                // Если есть выбранный тип операции - фильтруем категории
                if (transactionTypeId) {
                    filterCategories(transactionTypeId);
                }

                // Если есть выбранная категория - фильтруем подкатегории
                if (categoryId) {
                    filterSubcategories(categoryId);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error loading categories data:', error);
                console.log('Response:', xhr.responseText);
            }
        });

        // Обработчик изменения типа операции
        $('#id_transaction_type').change(function() {
            var transactionTypeId = $(this).val();
            console.log('Transaction type changed to:', transactionTypeId);
            filterCategories(transactionTypeId);
        });

        // Обработчик изменения категории
        $('#id_category').change(function() {
            var categoryId = $(this).val();
            console.log('Category changed to:', categoryId);
            filterSubcategories(categoryId);
        });
    });

})(django.jQuery);