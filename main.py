import json

import requests as requests

from src.DBManager import DBManager
from src.api import HeadHunterAPI

mylist = ["Coffeeshop Сompany (Кофешоп Компани)", "ООО Cибирская сбытовая компания",
          "ООО Cтраховая брокерская компания Альтернатива", "UPRO GROUP Гостиничная управляющая компания",
          "iiko, Компания Aйко", "АйБи Групп, группа компаний", "АО Алтайская Машиностроительная Компания",
          "Алтайская Рыбная Компания", "Архитектурно-брендинговая компания DEVISION",
          "АО Башкирская содовая компания", "ООО Виттория Компани", "ООО Волго-Камская Инжиниринговая Компания",
          "Группа Компаний 369", "ООО 1221Системс ", "ООО 1 Московская Зеркальная фабрика ", "1С-АВТОМАТИЗАЦИЯ ",
          "ООО 25 микрон ", "ООО 32 КАРАТА ", "ООО 360 КОНСТРАКШН ", "3DTEMa ", "ООО 3С Групп ",
          "АО 48 Управление Наладочных Работ ", "АО 47 Центральный Проектно-Изыскательский Институт ", "4 Колеса"]

hh = HeadHunterAPI(mylist)
my_list_of_vacancies = hh.create_list_vacancies()

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
