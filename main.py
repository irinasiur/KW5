import json

import requests as requests

from src.api import HeadHunterAPI

mylist = ["Coffeeshop Сompany (Кофешоп Компани)", "ООО Cибирская сбытовая компания",
          "ООО Cтраховая брокерская компания Альтернатива", "UPRO GROUP Гостиничная управляющая компания",
          "iiko, Компания Aйко", "АйБи Групп, группа компаний", "АО Алтайская Машиностроительная Компания",
          "Алтайская Рыбная Компания", "Архитектурно-брендинговая компания DEVISION",
          "АО Башкирская содовая компания", "ООО Виттория Компани", "ООО Волго-Камская Инжиниринговая Компания",
          "Группа Компаний 369"]

# mylist = ["ООО 1221Системс", "ООО Cибирская сбытовая компания", "ООО 1 Московская Зеркальная фабрика"]

hh = HeadHunterAPI(mylist)
my_list_of_vacancies = hh.create_list_vacancies()
for i in range(len(my_list_of_vacancies)):
    print(str(my_list_of_vacancies[i]))  # __str__())
# print(hh.get_vacancy_url())
