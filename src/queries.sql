1.
            SELECT c.company_name, COUNT(c.company_name)
            FROM vacancies v
            JOIN companies c
            ON v.company_id = c.company_id
            GROUP BY c.company_name
            ORDER BY c.company_name;
2.
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
3.
            SELECT
                ROUND(AVG(min_salary), 2),
                ROUND(AVG(max_salary), 2)
            FROM
                vacancies;
4.
            SELECT v.vacancy_name
            FROM vacancies v
            WHERE v.max_salary > (SELECT AVG(max_salary) FROM vacancies)
            AND v.min_salary > (SELECT AVG(min_salary) FROM vacancies);
5.
            SELECT v.vacancy_name
            FROM vacancies v
            WHERE LOWER(v.vacancy_name) LIKE '%{keyword.lower()}%';
