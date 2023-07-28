class Vacancy:

    def __init__(self, vacancy_name: str, min_salary: list, company_name: str, vacancy_url: str, company_id: int):
        self.vacancy_name = vacancy_name
        self.min_salary = min_salary
        self.company_name = company_name
        self.vacancy_url = vacancy_url
        self.company_id = company_id

    def __str__(self) -> str:
        """
        Возвращает название вакансии, минимальный уровень зарплаты в рублях,
        максимальный уровень зарплаты в рублях, название компании, ссылку на данную вакансию, id компании.
        """
        return f'"vacancy_name": {self.vacancy_name}' \
               f' "min_salary": {self.min_salary}' \
               f' "company_name": {self.company_name}' \
               f' "vacancy_url": {self.vacancy_url}' \
               f' "company_id": {self.company_id}'
