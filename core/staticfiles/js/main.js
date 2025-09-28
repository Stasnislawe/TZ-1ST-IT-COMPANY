// static/js/main.js - ПРОСТОЙ И РАБОЧИЙ ВАРИАНТ

$(document).ready(function() {
    // Базовые функции для работы интерфейса

    // Подтверждение удаления
    $('.confirm-delete').on('click', function() {
        return confirm('Вы уверены, что хотите удалить эту запись?');
    });

    // Автоматическое закрытие alert через 5 секунд
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);

    // Инициализация tooltips (если есть)
    if ($('[data-bs-toggle="tooltip"]').length > 0) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Функции для фильтрации на главной странице
function applyFilters() {
    $('#filter-form').submit();
}

function resetFilters() {
    $('#filter-form').find('input[type="text"], input[type="date"], select').val('');
    $('#filter-form').submit();
}