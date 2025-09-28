$(document).ready(function() {
    // Работаем только на страницах с формой записи
    if (!$('#record-form').length) return;

    // Автоматически устанавливаем текущую дату при создании новой записи
    if (window.location.pathname.indexOf('/create/') !== -1) {
        var today = new Date();

        // Форматируем дату для input type="date" (YYYY-MM-DD)
        var year = today.getFullYear();
        var month = String(today.getMonth() + 1).padStart(2, '0');
        var day = String(today.getDate()).padStart(2, '0');

        var currentDate = year + '-' + month + '-' + day;

        // Устанавливаем значение, только если поле пустое
        var dateField = $('#id_created_date');
        if (!dateField.val()) {
            dateField.val(currentDate);
        }
    }

    // НЕ выполняем загрузку категорий при первоначальной загрузке страницы
    // Вместо этого просто инициализируем обработчики событий

    // Простая функция для загрузки категорий
    function loadCategories(transactionTypeId) {
        if (transactionTypeId) {
            $.get('/ajax/load-categories/', {transaction_type_id: transactionTypeId}, function(data) {
                var categorySelect = $('#id_category');
                var currentCategoryId = categorySelect.val(); // Сохраняем текущее значение

                categorySelect.empty();
                categorySelect.append('<option value="">---------</option>');

                $.each(data, function(index, category) {
                    var selected = (category.id == currentCategoryId) ? 'selected' : '';
                    categorySelect.append('<option value="' + category.id + '" ' + selected + '>' + category.name + '</option>');
                });

                // Если категория была выбрана, загружаем подкатегории
                if (currentCategoryId) {
                    loadSubcategories(currentCategoryId);
                } else {
                    $('#id_subcategory').empty().append('<option value="">---------</option>');
                }
            });
        } else {
            $('#id_category').empty().append('<option value="">---------</option>');
            $('#id_subcategory').empty().append('<option value="">---------</option>');
        }
    }

    // Простая функция для загрузки подкатегорий
    function loadSubcategories(categoryId) {
        if (categoryId) {
            $.get('/ajax/load-subcategories/', {category_id: categoryId}, function(data) {
                var subcategorySelect = $('#id_subcategory');
                var currentSubcategoryId = subcategorySelect.val(); // Сохраняем текущее значение

                subcategorySelect.empty();
                subcategorySelect.append('<option value="">---------</option>');

                $.each(data, function(index, subcategory) {
                    var selected = (subcategory.id == currentSubcategoryId) ? 'selected' : '';
                    subcategorySelect.append('<option value="' + subcategory.id + '" ' + selected + '>' + subcategory.name + '</option>');
                });
            });
        } else {
            $('#id_subcategory').empty().append('<option value="">---------</option>');
        }
    }

    // Обработчики изменений
    $('#id_transaction_type').change(function() {
        loadCategories($(this).val());
    });

    $('#id_category').change(function() {
        loadSubcategories($(this).val());
    });

    // УДАЛЕНО: автоматическая загрузка категорий при загрузке страницы
    // Это позволяет серверным значениям оставаться нетронутыми

    // Простая валидация формы
    $('#record-form').on('submit', function(e) {
        var isValid = true;
        var errors = [];

        // Проверяем обязательные поля
        var requiredFields = [
            {id: '#id_created_date', name: 'Дата создания'},
            {id: '#id_transaction_type', name: 'Тип операции'},
            {id: '#id_category', name: 'Категория'},
            {id: '#id_subcategory', name: 'Подкатегория'},
            {id: '#id_amount', name: 'Сумма'}
        ];

        requiredFields.forEach(function(field) {
            var value = $(field.id).val();
            if (!value || value === '') {
                $(field.id).addClass('is-invalid');
                errors.push('Поле "' + field.name + '" обязательно для заполнения');
                isValid = false;
            } else {
                $(field.id).removeClass('is-invalid');
            }
        });

        // Проверка суммы
        var amountValue = $('#id_amount').val();
        if (amountValue) {
            var amount = parseFloat(amountValue.toString().replace(',', '.'));
            if (isNaN(amount) || amount <= 0) {
                $('#id_amount').addClass('is-invalid');
                errors.push('Сумма должна быть положительным числом');
                isValid = false;
            }
        }

        if (!isValid) {
            e.preventDefault();

            // Показываем ошибки
            var errorHtml = '<div class="alert alert-danger"><strong>Ошибки:</strong><ul>';
            errors.forEach(function(error) {
                errorHtml += '<li>' + error + '</li>';
            });
            errorHtml += '</ul></div>';

            // Удаляем старые ошибки
            $('.alert-danger').remove();

            // Добавляем новые ошибки в начало формы
            $('#record-form').prepend(errorHtml);

            // Прокручиваем к ошибкам
            $('html, body').animate({
                scrollTop: $('.alert-danger').offset().top - 100
            }, 500);
        }

        return isValid;
    });

    // Сброс ошибок при изменении полей
    $('input, select').on('input change', function() {
        $(this).removeClass('is-invalid');
    });
});