# Запуск

К сожалению на используемых нами сайтах нужно нажимать кнопки для открытия большего количества новостей.
Поэтому пришлось воспользоваться ботом и вам для запуска понадобится библиотека Selenium.

Если надо брать новости с Interfax'a, то понадобится Geckodriver и Firefox. 
Его можно скачать по ссылке: https://github.com/mozilla/geckodriver/releases.
После скачивания необходимо добавить geckodriver в PATH. Затем в файле interfaxParser.py в
переменную profile_path, выставить путь для своей системы, аналогичный приведённому.
После работы программа создаст файл interfax_news.json, в котором будут все записанные новости



# API:

Для работы Api понадобится Flask и flask_httpauth для аутентификации.

### Параметры для запроса:

    1. date - дата начиная с которой ищутся новости.
    Формат: day.month.year (08.10.2022)

    2. who - должность того, кто хочет увидеть новости:
    1 - директор, 2 - бухгалтер

    3. count - количество новостей которое хочет увидеть пользователь, может быть выведено меньше если не хватает. 
    По умолчанию равно трём

В api сделана небольшая система авторизации, есть два пользователя "admin" и "user". Для админа пароль "pigs", для
"user" пароль "pass".

Стоит обратить внимание, что одна и та же новость может быть выдана и для бухгалтера и для директора. Берутся все
подходящие новости, сортируются по рейтингу и выдаётся count лучших новостей по рейтингу.

### Пример запросов для api:

Увидеть записи начиная с 05.10.2022, новости для директора, количество новостей - 4

    curl -u admin:pigs -i "http://127.0.0.1:5000/vtb/api/v1.0/news?date=05.10.2022&who=1&count=2"

Ответ от api:

    {
    "news": [
        {
        "URL": "https://russian.rt.com/business/article/1057792-evropa-rossiya-sankcii-neft-ceny-potolok",
        "Title": "«В реальности не будет соблюдаться»: Евросоюз одобрил введение потолка цен на российскую нефть",
        "Date": "2022-10-06"
        },
        {
        "URL": "https://ria.ru/20221007/predprinimateli-1822332527.html",
        "Title": "Московские предприниматели запустили проект \"Своих не бросаем\"",
        "Date": "2022-10-07"
        }
    ]
    }

Увидеть записи начиная с 05.09.2022, новости для бухгалтера, количество новостей - 3 (используются значения по
умолчанию)

    curl -u user:pass -i "http://127.0.0.1:5000/vtb/api/v1.0/news?date=05.09.2022&who=2"

Ответ:

    {
    "news": [
        {
        "URL": "https://lenta.ru/news/2022/10/07/snij/",
        "Title": "В России стало меньше официальных безработных",
        "Date": "2022-10-08"
        },
        {
        "URL": "https://russian.rt.com/business/article/1055338-rubl-evro-kurs-snizhenie",
        "Title": "Впервые с октября 2014 года: курс евро на Мосбирже опустился до 51 рубля",
        "Date": "2022-09-30"
        },
        {
        "URL": "https://russian.rt.com/business/article/1057792-evropa-rossiya-sankcii-neft-ceny-potolok",
        "Title": "«В реальности не будет соблюдаться»: Евросоюз одобрил введение потолка цен на российскую нефть",
        "Date": "2022-10-06"
        }
    ]
    }
