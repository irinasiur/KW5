# Описание программы

Данная программа взаимодействует с сервисом HeadHunter, используя его API, для получения информации о вакансиях компаний. Затем программа сохраняет полученные данные в базу данных PostgreSQL и выполняет несколько запросов для анализа и вывода результатов.

## Установка и использование

1. Убедитесь, что у вас установлен Python 3 и библиотека psycopg2 для взаимодействия с базой данных PostgreSQL. Если библиотека не установлена, выполните команду:

```bash
pip install psycopg2
```

Перед использованием программы, убедитесь, что у вас есть база данных PostgreSQL, в которую будут сохраняться данные. 
Укажите параметры подключения к базе данных (хост, пользователь, пароль и имя базы данных) в файле src/DBManager.py.

Запустите программу, выполнив следующую команду:

```bash
python main.py
```
Функциональность программы
Получение списка компаний с вакансиями и их данных из API HeadHunter.
Создание и заполнение таблиц в базе данных PostgreSQL для компаний и вакансий.
Выполнение нескольких SQL-запросов для анализа данных и вывод результатов на экран.


Как использовать методы DBManager

# Удаляем таблицы, если они существуют
DBManager.drop_tables()

# Создаем таблицы
DBManager.create_tables()

# заполняем таблицы
DBManager.populate_companies(mylist)
DBManager.populate_vacancies(my_list_of_vacancies)

# выводим список всех компаний и количество вакансий у каждой компании
result = DBManager.get_companies_and_vacancies_count()
if result:
    print("\n\n 1. список всех компаний и количество вакансий у каждой компании: ")
    for row in result:
        row_text = '\t'.join(str(item) for item in row)
        print(row_text)

# выводим список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
result = DBManager.get_all_vacancies()
if result:
    print(
        "\n\n 2. список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию: ")
    for row in result:
        row_text = '\t'.join(str(item) for item in row)
        print(row_text)

# выводим среднюю зарплату по вакансиям (средняя максимальная, средняя минимальная)
result = DBManager.get_avg_salary()
print("\n\n 3. средняя минимальная и максимальная зарплата по вакансиям: ")
print(result)

# выводим список всех вакансий, у которых зарплата выше средней по всем вакансиям
result = DBManager.get_vacancies_with_higher_salary()
if result:
    print(
        "\n\n 4. список всех вакансий, у которых зарплата выше средней по всем вакансиям: ")
    for row in result:
        row_text = '\t'.join(str(item) for item in row)
        print(row_text)

# выводим список всех вакансий, в названии которых содержатся переданные в метод слова  например 'python'
result = DBManager.get_vacancies_with_keyword('бухгалтер')
if result:
    print(
        "\n\n 5. список всех вакансий, в названии которых содержатся переданные в метод слова: ")
    for row in result:
        row_text = '\t'.join(str(item) for item in row)
        print(row_text)


