import psycopg2

import psycopg2


class DBManager:
    _host = "localhost"
    _database = "kw5"
    _user = "myuser"
    _password = "mypass"

    @classmethod
    def connect(cls):
        """
        Метод подключения к базе данных PostgreSQL.
        """
        try:
            connection = psycopg2.connect(
                host=cls._host,
                user=cls._user,
                password=cls._password,
                dbname=cls._database
            )
            print("Успешное подключение к базе данных.")
            return connection
        except psycopg2.Error as e:
            print("Ошибка при подключении к базе данных:", e)
            return None

    @classmethod
    def drop_tables(cls):
        """
        Метод для удаления таблиц 'companies' и 'vacancies' из базы данных.
        """
        connection = cls.connect()
        if connection is None:
            return

        with connection.cursor() as cursor:
            try:
                # Удаляем таблицу vacancies, если она существует
                cursor.execute("DROP TABLE IF EXISTS vacancies CASCADE;")

                # Удаляем таблицу companies, если она существует
                cursor.execute("DROP TABLE IF EXISTS companies CASCADE;")
                print("Таблицы 'companies' и 'vacancies' удалены.")
            except psycopg2.Error as e:
                print("Ошибка при выполнении запроса:", e)

        connection.commit()
        connection.close()

    @classmethod
    def create_tables(cls):
        """
        Метод для создания таблиц 'companies' и 'vacancies' в базе данных.
        """
        connection = cls.connect()
        if connection is None:
            return

        with connection.cursor() as cursor:
            try:
                # Создаем таблицу companies
                cursor.execute('''
                        CREATE TABLE companies
                        (
                            company_id serial,
                            company_name varchar(255),
                            CONSTRAINT pk_companies_company_id PRIMARY KEY (company_id)
                        );
                    ''')

                # Создаем таблицу vacancies
                cursor.execute('''
                        CREATE TABLE vacancies
                        (
                            company_id int,
                            vacancy_id serial,
                            vacancy_name varchar(255),
                            min_salary int DEFAULT 0,
                            max_salary int DEFAULT 0,
                            vacancy_url varchar(255),
                            CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id),
                            CONSTRAINT fk_vacancies_companies FOREIGN KEY(company_id) REFERENCES companies(company_id)
                        );
                    ''')

                print("Таблицы 'companies' и 'vacancies' созданы.")
            except psycopg2.Error as e:
                print("Ошибка при выполнении запроса:", e)

        connection.commit()
        connection.close()

    @classmethod
    def populate_companies(cls, my_list):
        """
        Метод для заполнения таблицы companies из списка my_list с именами компаний.
        """
        connection = cls.connect()
        if connection is None:
            return

        with connection.cursor() as cursor:
            try:
                # Заполняем таблицу companies из списка my_list
                for company_name in my_list:
                    cursor.execute('INSERT INTO companies (company_name) VALUES (%s);', (company_name,))

                print("Таблица 'companies' заполнена.")
            except psycopg2.Error as e:
                print("Ошибка при выполнении запроса:", e)

        connection.commit()
        connection.close()

    @classmethod
    def populate_vacancies(cls, my_list_of_vacancies):
        """
        Метод для заполнения таблицы vacancies из списка my_list_of_vacancies.
        """
        connection = cls.connect()
        if connection is None:
            return

        with connection.cursor() as cursor:
            try:
                # Заполняем таблицу vacancies из списка my_list_of_vacancies
                for vacancy in my_list_of_vacancies:
                    # Получаем company_id по имени компании
                    cursor.execute('SELECT company_id FROM companies WHERE company_name = %s;', (vacancy.company_name,))
                    company_id = cursor.fetchone()

                    # Если компания существует, используем company_id для вставки данных в vacancies
                    if company_id is not None:
                        company_id = company_id[0]
                        cursor.execute(
                            'INSERT INTO vacancies (company_id, vacancy_name, min_salary, max_salary, vacancy_url) VALUES (%s, %s, %s, %s, %s);',
                            (
                                company_id,
                                vacancy.vacancy_name,
                                vacancy.min_salary[0],
                                vacancy.min_salary[1],
                                vacancy.vacancy_url
                            ))

                print("Таблица 'vacancies' заполнена.")
            except psycopg2.Error as e:
                print("Ошибка при выполнении запроса:", e)

        connection.commit()
        connection.close()

        """получает список всех компаний и количество вакансий у каждой компании."""

    @classmethod
    def get_companies_and_vacancies_count(cls):
        """получает список всех компаний и количество вакансий у каждой компании."""
        connection = cls.connect()
        if connection is None:
            return None

        query = """
            SELECT c.company_name, COUNT(c.company_name) 
            FROM vacancies v
            JOIN companies c
            ON v.company_id = c.company_id
            GROUP BY c.company_name
            ORDER BY c.company_name;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None
        finally:
            connection.close()

    @classmethod
    def get_all_vacancies(cls):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        connection = cls.connect()
        if connection is None:
            return None

        query = """
            SELECT
                v.vacancy_name,
                c.company_name,
                v.min_salary,
                v.max_salary,
                v.vacancy_url
            FROM
                vacancies v
            JOIN
                companies c ON v.company_id = c.company_id
            ORDER BY
                v.vacancy_name;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None
        finally:
            connection.close()

    @classmethod
    def get_avg_salary(cls):
        """получает среднюю зарплату по вакансиям."""
        connection = cls.connect()
        if connection is None:
            return None

        query = """
            SELECT
                ROUND(AVG(min_salary), 2),
                ROUND(AVG(max_salary), 2)
            FROM
                vacancies;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None
        finally:
            connection.close()

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        connection = cls.connect()
        if connection is None:
            return None

        query = """
            SELECT v.vacancy_name
            FROM vacancies v
            WHERE v.max_salary > (SELECT AVG(max_salary) FROM vacancies)
            AND v.min_salary > (SELECT AVG(min_salary) FROM vacancies);

        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None
        finally:
            connection.close()

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'."""
        connection = cls.connect()
        if connection is None:
            return None

        query = f"""
            SELECT v.vacancy_name
            FROM vacancies v
            WHERE LOWER(v.vacancy_name) LIKE '%{keyword.lower()}%';
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None
        finally:
            connection.close()
