<h1 align=center>Тестовое задание: Веб-сервис для управления движением денежных средств (ДДС)</h1>

<p align=center>Ссылка на ТЗ -> https://drive.google.com/file/d/1vbPk2aiMe52pDFW57zMUDMaW7rqrHypc/view</p>

<hr>

<h2 align=center>Инструкция по запуску (В БД уже есть записи для визуализации и тестирования, если нужна пустая БД - см. пункт 3)</h2>

<h3>1. Без Docker`a (инструкция по докеру ниже)</h3>
<p>git clone https://github.com/Stasnislawe/TZ-1ST-IT-COMPANY</p>
<p>cd core</p>
<p>pip install -r requirements.txt</p>
<p>python manage.py runserver</p>
<p>Ждём запуска, логинимся в админке - http://127.0.0.1:8000/admin/</p>
<p>Пароль и логин от админки -> stas stas</p>
<p>Управление справочниками, записями ДДС либо через интерфейс http://127.0.0.1:8000/ либо через админ-панель http://127.0.0.1:8000/admin/</p>
<p>Апи - http://127.0.0.1:8000/api/</p>

<hr>

<h3>2. Через Docker</h3>
<p>git clone https://github.com/Stasnislawe/TZ-1ST-IT-COMPANY</p>
<p>cd core </p>
<p></p>docker-compose up --build</p>
<p>Ждём запуска, логинимся в админке - http://127.0.0.1:8000/admin/</p>
<p>Пароль и логин от админки -> stas stas</p>
<p>Управление справочниками, записями ДДС либо через интерфейс http://127.0.0.1:8000/ либо через админ-панель http://127.0.0.1:8000/admin/</p>
<p>Апи - http://127.0.0.1:8000/api/</p>

<hr>

<h3>3. Если нужна чистая БД</h3>
<p>git clone https://github.com/Stasnislawe/TZ-1ST-IT-COMPANY</p>
<p>cd core </p>
<p>Удаляем БД - db.sqlite3 и все миграции в директории web/migrations</p>
<p>Создаём миграции - python manage.py makemigrations</p>
<p>Приминяем миграции - python manage.py migrate<p>
<p>Создаём суперпользователя - python manage.py createsuperuser</p>
<p>Запускаем сервер - python manage.py runserver<p>
<p>Ждём запуска, логинимся в админке - http://127.0.0.1:8000/admin/</p>
<p>Управление справочниками, записями ДДС либо через интерфейс http://127.0.0.1:8000/ либо через админ-панель http://127.0.0.1:8000/admin/</p>
<p>Апи - http://127.0.0.1:8000/api/</p>

<hr>

<h2>Это веб-приложение, разработанное на Django, для учета и управления движением денежных средств. Оно позволяет пользователям создавать, просматривать, редактировать и удалять записи о денежных операциях, а также управлять справочниками статусов, типов, категорий и подкатегорий.</h2>

<h3>Основные возможности</h3>
<li>Управление записями ДДС: Создание, просмотр, редактирование и удаление записей о движении денежных средств.</li>

<li>Фильтрация записей: Поддержка фильтрации по дате, статусу, типу, категории и подкатегории.</li>

<li>Управление справочниками: Добавление, редактирование и удаление статусов, типов, категорий и подкатегорий с установлением логических зависимостей.</li>

<h3>Логические зависимости:</h3>

<li>Подкатегории привязаны к категориям.</li>

<li>Категории привязаны к типам.</li>

<h3>Технологии:</h3>
<li>Backend: Django, Django ORM</li>

<li>Frontend: HTML, CSS (Bootstrap), JavaScript</li>

<li>База данных: SQLite (по умолчанию)</li>

<h3>Особенности:</h3>
<li>Возможность создавать/редактировать/удалять как через админку, так и через приятный интерфейс</li>
<li>Тесты: Моделей, Форм, Вьюх, Апи, Интеграционные тесты</li>
<li>Фильтрация в админке, в интерфейсе, в апи</li>
<li>В Апи статистика: по месяцам, по категориям, сводная статистика</li>
<li>Контейнеризация Docker</li>

<h3>Недопонимания с описанием ТЗ</h3>
<li>Нужно ли было делать регистрацию/авторизацию пользователей или достаточно обычного входа через админку</li>
<li>В оценочных критериях есть упоминание Django Rest Framework, при этом про API ничего не было сказано (минимальный REST API добавил)</li>

<hr>

<h2 align=center>Скриншоты:</h2>
<h2 align=center>Общий вид интерфейса</h2>
<img width="1199" height="941" alt="image" src="https://github.com/user-attachments/assets/3e57e3e9-35af-42ec-8b50-672d454b2e1a" />
<h2 align=center>Фильтрация</h2>
<img width="1194" height="500" alt="image" src="https://github.com/user-attachments/assets/d8888fb2-62e9-4c29-b276-1c4d86f90c0c" />
<h2 align=center>Создание новоей записи ДДС</h2>
<img width="1196" height="670" alt="image" src="https://github.com/user-attachments/assets/3b29f78a-fc22-46a6-9687-b2c5ef3f40a1" />
<h2 align=center>Справочники</h2>
<img width="1194" height="512" alt="image" src="https://github.com/user-attachments/assets/a876d2b6-44ce-468b-b98c-f54f9a6296f5" />
<h2 align=center>Редактирование справочников на примере "Статуса"</h2>
<img width="1190" height="414" alt="image" src="https://github.com/user-attachments/assets/fbd51708-8454-466f-9b95-f5f356efff96" />
<h2 align=center>Список API</h2>
<img width="195" height="367" alt="image" src="https://github.com/user-attachments/assets/081c7a26-15cc-46ea-ba31-38f20540b881" />
<h2 align=center>Админка</h2>
<img width="845" height="644" alt="image" src="https://github.com/user-attachments/assets/f5e3c29b-7eea-4c24-8d87-afbc487f3846" />



