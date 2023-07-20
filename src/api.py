import json
import requests

from src.vacancy import Vacancy


# from vacancy import Vacancy


class HeadHunterAPI:
    """
    Класс для работы с API сайта headhunter.ru.
    """

    def __init__(self, mylist):
        """
        Магический метод для инициализации экземпляров класса, класс инициализируется списком компаний.
        """
        self.mylist = mylist

    def get_vacancy_url(self) -> dict:
        """
        В методе задана переменная  site, которая содержит API endpoint, метод возвращает словарь в виде:
        имя компании: url, по которому доступны вакансии этой компании.
        """
        site = "https://api.hh.ru/employers"
        out_dict = {}
        params = {}
        for company in self.mylist:
            params = {'text': company}
            if requests.get(site).status_code == 200:
                out_dict[company] = json.loads(requests.get(site, params).content.decode())['items'][0]['vacancies_url']
        return out_dict

    def parse_vacancy_url(self, url: str):
        """
        Получает url и возвращает  json объект.
        """

        site = url
        if requests.get(site).status_code == 200:
            return json.loads(requests.get(site).content.decode())

    def create_list_vacancies(self):
        """
        В методе мы в цикле проходим по всему словарю get_vacancy_url, получаем значения
        (url, по которому доступны вакансии этой компании)
        с помощью метода parse_vacancy_url получаем JSON объекты, забираем из них необходимые данные для инициализации
        экземпляров класса Vacancy.
        :return: список экземпляров класса Vacancy.
        """
        keys = self.get_vacancy_url()
        vacancies = []
        for k in keys:
            json_object = self.parse_vacancy_url(keys.get(k))
            part_to_parse = json_object["items"]
            for i in range(len(part_to_parse)):
                vacancy_name = part_to_parse[i]["name"] if part_to_parse[i]["name"] is not None else "0"
                if part_to_parse[i]["salary"] == "null":
                    min_salary = 0
                    max_salary = 0
                else:
                    min_salary = part_to_parse[i]["salary"]["from"] if part_to_parse[i]["salary"]["from"] is not None else 0
                    max_salary = part_to_parse[i]["salary"]["to"] if part_to_parse[i]["salary"]["to"] is not None else 0
                company_name = part_to_parse[i]["employer"]["name"] \
                    if part_to_parse[i]["employer"]["name"] is not None else "0"
                vacancy_url = part_to_parse[i]["alternate_url"] \
                    if part_to_parse[i]["alternate_url"] is not None else "0"
                vacancy = Vacancy(vacancy_name, [min_salary, max_salary], company_name, vacancy_url, None)
                vacancies.append(vacancy)
        return vacancies


