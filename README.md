### Описание:

PAY2U — менеджер платных подписок.

«PAY2U»: помогает вести учет ваших подписок, отслеживть все свои подписки в одном приложении. Подписку на сервис можно добавить из каталога, найти нужный сервис по категори или через поиск. В приложении ведеться аналитика подписок, расходы на подписки, сумма кэшбэка в этом месяце, сумма которую предстоит заплатить за подписки в этом месяце. К каждому сервису прилогаеться описание всех доступных тарифов, а так же есть возможность добавить в список сравнения.

### Как запустить проект:

## Локальный запуск проекта:
```
Клонируйте репозиторий с проектом на свой компьютер. В терминале из рабочей директории выполните команду:

git clone https://git@github.com:FrolovAlex22/PAY2U.git

```
Cоздать и активировать виртуальное окружение:

Команда для установки виртуального окружения на Mac или Linux:

python3 -m venv env
source env/bin/activate

Команда для Windows:

python -m venv venv
source venv/Scripts/activate

```
Перейти в директорию devops:

cd devops

Создать файл .env по образцу:

.env.example

```
Установить зависимости из файла requirements.txt

cd ..
cd backend
pip install -r requirements.txt

```
Выполните миграции:

python manage.py migrate

```
Создание нового супер пользователя:

python manage.py createsuperuser

```
Заполните базу тестовыми данными:

python manage.py categorys

```
Запустить локальный сервер:

python manage.py runserver

## Установка на удалённом сервере:
```
Выполнить вход на удаленный сервер

Установить docker:

sudo apt install docker.io

```
Установить docker-compose:

sudo apt install docker-compose    

```
Находясь локально в директории devops/, скопировать файлы docker-compose.yml и nginx.conf на удаленный сервер:

scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/

```
Выполните команду:

docker compose up 

```
Создайте и выполните миграции:

docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

```
Создайте суперпользователя:

docker-compose exec backend python manage.py createsuperuser

```
Загрузите статику:

docker-compose exec backend python manage.py collectstatic

```
Заполните базу тестовыми данными:

docker-compose exec backend python manage.py categorys

### Основные адреса:

```
Регистрация пользователя:

/api/user/

```
Получение данных своей учетной записи:

/api/user/profile/ 

```
Получение данных о кэшбэке в этом месяце:

/api/user/cashback/ 

```
Получение данных о предстоящих расходах в этом месяце:

/api/user/expenses/ 

```
Получение данных о оплаченых сервисах в этом месяце:

/api/user/paids/ 

```
Получение списка сервисов на который подписан ползователь:

/api/user/subscriptions/ 

```
Главная страница приложения:

/api/main/ 

```
Каталог сервисов:

/api/categories/catalog/

```
Список сервисов в определенной категории:

/api/categories/<id>/

```
Страница с лучшими предложениями:

/api/services/bestoffer/

```
Страница сервиса с описание:

/api/services/<id>/

```
Подписка на сервис:

/api/services/<id>/terms/<term_pk>/

```
Добавление подписки:

/api/services/<id>/terms/<term_pk>/subscribe/

```
Список сервисов в сравнении:

/api/comparison/

```
Добавить сервис в сравнении:

/api/services/add_comparison/

```

### Авторы:

Фролов Александр
email: frolov.bsk@yandex.ru
github: https://github.com/FrolovAlex22

```
Анастас Даниелян
email: danielyan.anastas@gmail.com
github: https://github.com/AnastasDan
