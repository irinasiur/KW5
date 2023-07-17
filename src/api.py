import json
from abc import ABC, abstractmethod
import requests


class API(ABC):
    """
    Класс для работы с API.
    """

    @abstractmethod
    def __init__(self):
        """
        Магический метод для инициализации экземпляров класса.
        """
        pass

    @abstractmethod
    def get_page(self):
        """
        Метод для получения страницы со списком вакансий.
        """
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API сайта headhunter.ru.
    """
    get_tag: str

    def __init__(self, vacancy_name: str, search_city: str):
        """
        Магический метод для инициализации экземпляров класса.
        """
        self.hh_vacancy_name = vacancy_name
        self.hh_city = search_city

    @staticmethod
    def get_anything(get_tag: str) -> dict:
        """
        Метод принимает endpoint API и возвращает json объект.
        """
        site = "https://api.hh.ru/"
        if requests.get(site + get_tag).status_code == 200:
            return json.loads(requests.get(site + get_tag).content.decode())

    def get_areas(self) -> dict:
        """
        Метод для получения словаря, в котором ключем является название города,
        значением является id этого города.
        """
        ar_dict = {}
        try:
            for k in self.get_anything("areas"):
                for i in range(len(k['areas'])):
                    if len(k['areas'][i]['areas']) != 0:  # Если у зоны есть внутренние зоны
                        for j in range(len(k['areas'][i]['areas'])):
                            ar_dict[k['areas'][i]['areas'][j]['name']] = k['areas'][i]['areas'][j]['id']
                    else:  # Если у зоны нет внутренних зон
                        ar_dict[k['areas'][i]['name']] = k['areas'][i]['id']
        except TypeError:
            print("get_tag не найден.")
        else:
            return ar_dict

    def get_page(self) -> dict:
        """
        Метод для получения страницы со списком вакансий.
        Аргументы:
            page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
            per_page - Количество вакансий на 1 странице, не может быть больше 100.
        Значение по умолчанию 100, т.е. максимально возможное количество.
        """
        try:
            params = {
                'text': 'NAME:' + self.hh_vacancy_name,
                # Текст фильтра. В имени должно быть название указанной вакансии
                'area': self.get_areas().get(self.hh_city),  # Поиск ощуществляется по вакансиям выбранного города
                'page': 0,  # Индекс страницы поиска на HH - 0
                'per_page': 100  # Кол-во вакансий на 1 странице
            }
        except AttributeError:
            print("get_tag не найден.")
        else:
            req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
            data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
            req.close()
            return json.loads(data)
